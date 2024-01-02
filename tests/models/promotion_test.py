from app.models.promotion import PromoCode
from app.models.restriction import DateRestriction, AgeRestriction, LogicalRestriction
from datetime import datetime


def create_date_str(year, month, day):
    return datetime(year, month, day).strftime("%Y-%m-%d")


def test_create_valid_promocode():
    """Test creating a valid PromoCode with a single restriction."""
    promo = PromoCode(
        name="SummerSale",
        avantage={"avantage_type": "percent", "value": 15},
        restrictions=[DateRestriction(
            after="2021-06-01", before="2021-08-31")],
    )
    promo.clean()


def test_promocode_with_logical_restriction():
    """Test creating a PromoCode with a logical 'or' restriction."""
    promo = PromoCode(
        name="SpecialOffer",
        avantage={"avantage_type": "discount", "value": 15},
        restrictions=[
            LogicalRestriction(
                restrictions=[
                    DateRestriction(after="2021-11-01", before="2021-12-31"),
                    AgeRestriction(gt=30),
                ]
            )
        ],
    )
    promo.clean()


def test_save_and_retrieve_promocode(mongodb_connection):
    """Test saving a PromoCode to the database and retrieving it."""
    promo_name = "SummerSale"
    promo = PromoCode(
        name=promo_name,
        avantage={"avantage_type": "percent", "value": 15},
        restrictions=[DateRestriction(
            after="2021-06-01", before="2021-08-31")],
    )
    promo.save()  # Save the PromoCode to the database

    # Retrieve the saved PromoCode
    retrieved_promo = PromoCode.objects(name=promo_name).first()

    assert retrieved_promo is not None
    assert retrieved_promo.name == promo_name
