from mongoengine import Document, StringField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, DictField
from mongoengine import ValidationError


class BaseRestriction(EmbeddedDocument):
    """abstract base class for all types of restrictions"""
    meta = {'allow_inheritance': True}


class DateRestriction(BaseRestriction):
    """Date restriction"""
    after = StringField()
    before = StringField()


class AgeRestriction(BaseRestriction):
    """Age restriction"""
    eq = IntField()
    lt = IntField()
    gt = IntField()


class TempRestriction(BaseRestriction):
    """Temp restriction"""
    gt = StringField()
    lt = StringField()


class MeteoRestriction(BaseRestriction):
    """Meteo restriction"""
    is_ = StringField(db_field='is')
    temp = EmbeddedDocumentField(TempRestriction)


class LogicalRestriction(BaseRestriction):
    """used for "or" and "and" logical operators"""
    restrictions = ListField(EmbeddedDocumentField(BaseRestriction))

# main document


class PromoCode(Document):
    name = StringField(required=True)
    avantage = DictField()
    restrictions = ListField(EmbeddedDocumentField(BaseRestriction))

    meta = {'collection': 'weather_codes'}

    def clean(self):
        # Ensure that there is either one restriction or one logical restriction
        if len(self.restrictions) != 1:
            raise ValidationError(
                "WeatherCode must have exactly one restriction or one logical restriction")
