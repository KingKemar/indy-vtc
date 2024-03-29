from mongoengine import Document, StringField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField
from app.models.restriction import BaseRestriction, RestrictionFactory, RestrictionValidationError


class Avantage(EmbeddedDocument):
    """Class to represent the avantage of a PromoCode"""
    avantage_type = StringField(choices=['percent', 'discount'], required=True)
    value = IntField(required=True)

# main document


class PromoCode(Document):
    name = StringField(required=True, unique=True)
    avantage = EmbeddedDocumentField(Avantage)
    restrictions = ListField(EmbeddedDocumentField(BaseRestriction))

    meta = {'collection': 'weather_codes'}

    def check_restrictions(self, arguments):
        errors = []

        for restriction in self.restrictions:
            result = restriction.check_restrictions(arguments)
            if result:
                errors.append(result)

        if not errors:
            return None

        return RestrictionValidationError("AND", None, errors)

    @classmethod
    def from_json(cls, data):
        promo = cls()
        promo.name = data.get('name')
        avantage_data = data.get('avantage', {})
        if avantage_data:
            # Extract avantage_type and value
            avantage_type, value = next(iter(avantage_data.items()))
            promo.avantage = Avantage(avantage_type=avantage_type, value=value)

        restrictions_data = data.get('restrictions', [])
        promo.restrictions = [RestrictionFactory.create_restriction(
            r) for r in restrictions_data]

        return promo
