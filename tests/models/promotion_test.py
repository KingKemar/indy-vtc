import pytest
from app.models.promotion import (
    PromoCode, DateRestriction, AgeRestriction, LogicalRestriction,
    MeteoRestriction, ValidationError, Avantage
)
from datetime import datetime, timedelta


def create_date_str(year, month, day):
    return datetime(year, month, day).strftime('%Y-%m-%d')


def test_create_valid_promocode():
    """Test creating a valid PromoCode with a single restriction."""
    promo = PromoCode(
        name="SummerSale",
        avantage={"avantage_type": "percent",
                  "value": 15},
        restrictions=[DateRestriction(after="2021-06-01", before="2021-08-31")]
    )
    promo.clean()


def test_promocode_with_multiple_restrictions():
    """Test that a PromoCode with multiple restrictions raises ValidationError."""
    promo = PromoCode(
        name="SpringSale",
        avantage={"avantage_type": "percent",
                  "value": 10},
        restrictions=[
            DateRestriction(after="2021-03-01", before="2021-05-31"),
            AgeRestriction(eq=25)
        ]
    )
    with pytest.raises(ValidationError):
        promo.clean()


def test_promocode_with_logical_restriction():
    """Test creating a PromoCode with a logical 'or' restriction."""
    promo = PromoCode(
        name="SpecialOffer",
        avantage={"avantage_type": "discount",
                  "value": 15},
        restrictions=[
            LogicalRestriction(restrictions=[
                DateRestriction(after="2021-11-01", before="2021-12-31"),
                AgeRestriction(gt=30)
            ])
        ]
    )
    promo.clean()


def test_save_and_retrieve_promocode(mongodb_connection):
    """Test saving a PromoCode to the database and retrieving it."""
    promo_name = "SummerSale"
    promo = PromoCode(
        name=promo_name,
        avantage={"avantage_type": "percent",
                  "value": 15},
        restrictions=[DateRestriction(after="2021-06-01", before="2021-08-31")]
    )
    promo.save()  # Save the PromoCode to the database

    # Retrieve the saved PromoCode
    retrieved_promo = PromoCode.objects(name=promo_name).first()

    assert retrieved_promo is not None
    assert retrieved_promo.name == promo_name


# Test for DateRestriction check_restrictions method
def test_date_restriction_check():
    # Get today's date
    today = datetime.now().date()

    # Create dates for 7 days before and after today
    seven_days_before = today - timedelta(days=7)
    seven_days_after = today + timedelta(days=7)
    two_days_ago = today - timedelta(days=2)

    # Create a DateRestriction object valid from 7 days before to 7 days after today
    date_restriction = DateRestriction(
        after=seven_days_before.strftime('%Y-%m-%d'),
        before=seven_days_after.strftime('%Y-%m-%d')
    )
    assert date_restriction.check_restrictions(
        {}) == (True, [])

    # Modify the restriction to be valid only until 2 days ago
    date_restriction.before = two_days_ago.strftime('%Y-%m-%d')
    assert date_restriction.check_restrictions({}) == (
        False, [f"Promotion expired, was valid before {two_days_ago.strftime('%Y-%m-%d')}"])

# Test for AgeRestriction check_restrictions method


def test_age_restriction_check():
    age_restriction = AgeRestriction(eq=25)
    assert age_restriction.check_restrictions(
        {'age': 25}) == (True, [])
    assert age_restriction.check_restrictions({'age': 24})[0] == False

# Test for MeteoRestriction check_restrictions method


def test_meteo_restriction_check():
    meteo_restriction = MeteoRestriction(is_="sunny")
    assert meteo_restriction.check_restrictions(
        {'meteo': {'weather': ['sunny']}}) == (True, [])

    # Test with non-matching weather
    assert meteo_restriction.check_restrictions(
        {'meteo': {'weather': ['rainy']}})[0] == False

# Test for LogicalRestriction check_restrictions method


def test_logical_restriction_check():
    logical_restriction = LogicalRestriction(
        operator='or',
        restrictions=[
            DateRestriction(after="2021-06-01", before="2021-08-31"),
            AgeRestriction(eq=30)
        ]
    )
    # Test with one condition met
    assert logical_restriction.check_restrictions({'age': 30}) == (True, [])

    # Test with no condition met
    assert logical_restriction.check_restrictions({'age': 25})[0] == False

# Test for PromoCode check_restrictions method


def test_promocode_check_restrictions():
    promo = PromoCode(
        name="SpecialOffer",
        avantage=Avantage(avantage_type='percent', value=20),
        restrictions=[AgeRestriction(eq=25)]
    )
    # Test with matching age
    assert promo.check_restrictions({'age': 25}) == (True, [])

    # Test with non-matching age
    assert promo.check_restrictions({'age': 24})[0] == False
