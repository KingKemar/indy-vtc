from mongoengine import Document, StringField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, DictField
from mongoengine import ValidationError
from datetime import datetime


class BaseRestriction(EmbeddedDocument):
    """abstract base class for all types of restrictions"""
    meta = {'allow_inheritance': True}

    def check_restrictions(self, arguments):
        raise NotImplementedError(
            "Must implement check_restrictions in subclass")


class DateRestriction(BaseRestriction):
    """Date restriction"""
    after = StringField()
    before = StringField()

    def check_restrictions(self, arguments):
        # Get current date
        current_date = datetime.now().date()
        print(current_date)

        # Check and parse the 'after' date if it exists
        if self.after:
            after_date = datetime.strptime(self.after, '%Y-%m-%d').date()
            if current_date < after_date:
                return False, [f"Promotion not valid yet, starts after {self.after}"]

        # Check and parse the 'before' date if it exists
        if self.before:
            before_date = datetime.strptime(self.before, '%Y-%m-%d').date()
            if current_date > before_date:
                return False, [f"Promotion expired, was valid before {self.before}"]

        # If either 'after' or 'before' is not set, or if current date is within the range
        return True, []


class AgeRestriction(BaseRestriction):
    """Age restriction"""
    eq = IntField()
    lt = IntField()
    gt = IntField()

    def check_restrictions(self, arguments):
        user_age = arguments.get('age')

        # Check if the user's age is provided in the arguments
        if user_age is None:
            return False, ["Age not provided in arguments"]

        # Check 'eq' condition
        if self.eq is not None and user_age != self.eq:
            return False, [f"Age restriction not met, requires exactly {self.eq} years"]

        # Check 'lt' condition
        if self.lt is not None and user_age >= self.lt:
            return False, [f"Age restriction not met, requires less than {self.lt} years"]

        # Check 'gt' condition
        if self.gt is not None and user_age <= self.gt:
            return False, [f"Age restriction not met, requires greater than {self.gt} years"]

        return True, []


class TempRestriction(BaseRestriction):
    """Temp restriction"""
    gt = StringField()
    lt = StringField()

    def check_restrictions(self, arguments):
        current_temp = arguments.get('meteo', {}).get('temp')

        # Check if the temperature is provided in the arguments
        if current_temp is None:
            return False, ["Temperature not provided in arguments"]

        # Convert string fields to float for comparison
        gt_value = float(self.gt) if self.gt is not None else None
        lt_value = float(self.lt) if self.lt is not None else None

        # Check 'gt' condition
        if gt_value is not None and current_temp <= gt_value:
            return False, [f"Temperature restriction not met, requires greater than {gt_value} degrees"]

        # Check 'lt' condition
        if lt_value is not None and current_temp >= lt_value:
            return False, [f"Temperature restriction not met, requires less than {lt_value} degrees"]

        return True, []


class MeteoRestriction(BaseRestriction):
    """Meteo restriction"""
    is_ = StringField(db_field='is')
    temp = EmbeddedDocumentField(TempRestriction)

    def check_restrictions(self, arguments):
        current_weather = arguments.get('meteo', {}).get('weather')
        messages = []
        weather_check_message = None
        weather_check_result = True
        # Check weather condition
        if self.is_ is not None:
            if not current_weather:
                weather_check_result, weather_check_message = False, "Weather data not provided in arguments"

            if self.is_ not in current_weather:
                weather_check_result, weather_check_message = False, f"Weather condition '{self.is_}' not met. Current weather: {current_weather}"
            # if we are supposed to check theweather we append the error message if it exists
            if weather_check_message:
                messages.append(weather_check_message)

        # Check temperature condition if it exists
        if self.temp:
            temp_check_result, temp_message = self.temp.check_restrictions(
                arguments)
            # if we are supposed to check temperature
            # we update the value
            weather_check_result = weather_check_result and temp_check_result
            # we append the message
            if temp_message:
                messages.append(temp_message[0])
        return weather_check_result, messages


class LogicalRestriction(BaseRestriction):
    """used for "or" and "and" logical operators"""
    operator = StringField(choices=['and', 'or'], required=True)
    restrictions = ListField(EmbeddedDocumentField(BaseRestriction))

    def check_restrictions(self, arguments):
        if self.operator == 'and':
            return self._check_and_restrictions(arguments)
        elif self.operator == 'or':
            return self._check_or_restrictions(arguments)
        else:
            return False, ["Invalid logical operator"]

    def _check_and_restrictions(self, arguments):
        messages = []
        all_passed = True
        for restriction in self.restrictions:
            passed, msg = restriction.check_restrictions(arguments)
            all_passed &= passed  # AND logic
            messages.extend(msg)
        return all_passed, messages

    def _check_or_restrictions(self, arguments):
        messages = []
        any_passed = False
        for restriction in self.restrictions:
            passed, msg = restriction.check_restrictions(arguments)
            any_passed |= passed  # OR logic
            messages.extend(msg)
        if any_passed:
            return any_passed, []
        return any_passed, messages


class Avantage(EmbeddedDocument):
    """Class to represent the avantage of a PromoCode"""
    avantage_type = StringField(choices=['percent', 'discount'], required=True)
    value = IntField(required=True)

# main document


class PromoCode(Document):
    name = StringField(required=True)
    avantage = EmbeddedDocumentField(Avantage)
    restrictions = ListField(EmbeddedDocumentField(BaseRestriction))

    meta = {'collection': 'weather_codes'}

    def clean(self):
        # Ensure that there is either one restriction or one logical restriction
        if len(self.restrictions) != 1:
            raise ValidationError(
                "WeatherCode must have exactly one restriction or one logical restriction")

    def check_restrictions(self, arguments):
        if self.restrictions:
            return self.restrictions[0].check_restrictions(arguments)
        return True, []
