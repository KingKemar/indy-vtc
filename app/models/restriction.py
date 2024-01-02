from mongoengine import (
    StringField,
    IntField,
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ValidationError,
)
from datetime import datetime


class RestrictionValidationError:
    def __init__(self, type, message, children=None):
        self.type = type
        self.message = message
        self.children = children or []

    def add_child(self, child_error):
        self.children.append(child_error)

    def jsonify(self):
        error_data = {
            "type": self.type,
            "message": self.message,
            "children": [child.jsonify() for child in self.children],
        }
        return error_data


class BaseRestriction(EmbeddedDocument):
    """abstract base class for all types of restrictions"""

    meta = {"allow_inheritance": True}

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
            after_date = datetime.strptime(self.after, "%Y-%m-%d").date()
            if current_date < after_date:
                return RestrictionValidationError(
                    "Date", f"Promotion not valid yet, starts after {self.after}"
                )

        # Check and parse the 'before' date if it exists
        if self.before:
            before_date = datetime.strptime(self.before, "%Y-%m-%d").date()
            if current_date > before_date:
                return RestrictionValidationError(
                    "Date", f"Promotion expired, was valid before {self.before}"
                )

        # If either 'after' or 'before' is not set, or if current date is within the range
        return None

    def clean(self):
        # Convert strings to dates for comparison
        if self.after and self.before:
            after_date = datetime.strptime(self.after, "%Y-%m-%d").date()
            before_date = datetime.strptime(self.before, "%Y-%m-%d").date()

            # Check if 'before' date is actually after the 'after' date
            if before_date <= after_date:
                raise ValidationError(
                    "The 'before' date must be after the 'after' date."
                )


class AgeRestriction(BaseRestriction):
    """Age restriction"""

    eq = IntField()
    lt = IntField()
    gt = IntField()

    def check_restrictions(self, arguments):
        user_age = arguments.get("age")

        # Check if the user's age is provided in the arguments
        if user_age is None:
            return RestrictionValidationError("Age", "Age not provided in arguments")

        # Check 'eq' condition
        if self.eq is not None and user_age != self.eq:
            return RestrictionValidationError(
                "Age", f"Age restriction not met, requires exactly {self.eq} years"
            )

        # Check 'lt' condition
        if self.lt is not None and user_age >= self.lt:
            return RestrictionValidationError(
                "Age", f"Age restriction not met, requires less than {self.lt} years"
            )

        # Check 'gt' condition
        if self.gt is not None and user_age <= self.gt:
            return RestrictionValidationError(
                "Age", f"Age restriction not met, requires greater than {self.gt} years"
            )

        return None


class TempRestriction(BaseRestriction):
    """Temp restriction"""

    gt = StringField()
    lt = StringField()

    def check_restrictions(self, arguments):
        current_temp = arguments.get("meteo", {}).get("temp")

        # Check if the temperature is provided in the arguments
        if current_temp is None:
            return RestrictionValidationError(
                "Temperature", "Temperature not provided in arguments"
            )

        # Convert string fields to float for comparison
        gt_value = float(self.gt) if self.gt is not None else None
        lt_value = float(self.lt) if self.lt is not None else None

        # Check 'gt' condition
        if gt_value is not None and current_temp <= gt_value:
            return RestrictionValidationError(
                "Temperature",
                f"Temperature restriction not met, requires greater than {gt_value} degrees",
            )

        # Check 'lt' condition
        if lt_value is not None and current_temp >= lt_value:
            return RestrictionValidationError(
                "Temperature",
                f"Temperature restriction not met, requires less than {lt_value} degrees",
            )

        return True, []


class MeteoRestriction(BaseRestriction):
    """Meteo restriction"""

    is_ = StringField(db_field="is")
    temp = EmbeddedDocumentField(TempRestriction)

    def check_restrictions(self, arguments):
        current_weather = arguments.get("meteo", {}).get("weather")
        errors = []

        # Check weather condition
        if self.is_ is not None:
            if not current_weather:
                errors.append(
                    RestrictionValidationError(
                        "Meteo", "Weather data not provided in arguments"
                    )
                )
            elif self.is_ not in current_weather:
                errors.append(
                    RestrictionValidationError(
                        "Meteo",
                        f"Weather condition '{self.is_}' not met. Current weather: {current_weather}",
                    )
                )

        # Check temperature condition if it exists
        if self.temp:
            temp_result = self.temp.check_restrictions(arguments)
            if temp_result:
                errors.append(temp_result)

        if errors:
            return RestrictionValidationError("Meteo", None, errors)

        return None


class LogicalRestriction(BaseRestriction):
    """used for "or" and "and" logical operators"""

    operator = StringField(choices=["and", "or"], required=True)
    restrictions = ListField(EmbeddedDocumentField(BaseRestriction))

    def check_restrictions(self, arguments):
        errors = []

        for restriction in self.restrictions:
            result = restriction.check_restrictions(arguments)
            if result:
                errors.append(result)

        if not errors:
            return None

        return RestrictionValidationError(self.operator.upper(), None, errors)


class RestrictionFactory:
    @staticmethod
    def create_restriction(data):
        mapping = {
            "@date": DateRestriction,
            "@age": AgeRestriction,
            "@meteo": MeteoRestriction,
            "@or": LogicalRestriction,
            "@and": LogicalRestriction,
        }

        restriction_type = next(
            (key for key in mapping.keys() if key in data), None)

        if restriction_type:
            if restriction_type in ["@or", "@and"]:
                operator = "or" if restriction_type == "@or" else "and"
                restrictions = [
                    RestrictionFactory.create_restriction(r)
                    for r in data[restriction_type]
                ]
                return LogicalRestriction(operator=operator, restrictions=restrictions)
            else:
                return mapping[restriction_type](**data[restriction_type])

        raise ValueError("Invalid restriction type")
