from app.models.promotion import PromoCode, Avantage
from app.models.restriction import (
    DateRestriction,
    AgeRestriction,
    LogicalRestriction,
    MeteoRestriction,
)
from datetime import datetime, timedelta

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
        after=seven_days_before.strftime("%Y-%m-%d"),
        before=seven_days_after.strftime("%Y-%m-%d"),
    )
    assert date_restriction.check_restrictions({}) == None

    # Modify the restriction to be valid only until 2 days ago
    date_restriction.before = two_days_ago.strftime("%Y-%m-%d")
    assert (
        date_restriction.check_restrictions({}).message
        == f"Promotion expired, was valid before {two_days_ago.strftime('%Y-%m-%d')}"
    )


# Test for AgeRestriction check_restrictions method


def test_age_restriction_check():
    age_restriction = AgeRestriction(eq=25)
    assert age_restriction.check_restrictions({"age": 25}) == None
    assert age_restriction.check_restrictions({"age": 24}).type == "Age"


# Test for MeteoRestriction check_restrictions method


def test_meteo_restriction_check():
    meteo_restriction = MeteoRestriction(is_="sunny")
    assert (
        meteo_restriction.check_restrictions(
            {"meteo": {"weather": ["sunny"]}}) == None
    )

    # Test with non-matching weather
    assert (
        meteo_restriction.check_restrictions(
            {"meteo": {"weather": ["rainy"]}}).type
        == "Meteo"
    )


# Test for LogicalRestriction check_restrictions method


def test_logical_restriction_check():
    today = datetime.now().date()

    seven_days_before = today - timedelta(days=7)
    seven_days_after = today + timedelta(days=7)
    logical_restriction = LogicalRestriction(
        operator="or",
        restrictions=[
            DateRestriction(
                after=seven_days_before.strftime("%Y-%m-%d"),
                before=seven_days_after.strftime("%Y-%m-%d"),
            ),
            AgeRestriction(eq=30),
        ],
    )
    # Test with one condition met
    assert logical_restriction.check_restrictions({"age": 30}) is None

    # Test with no condition met
    validation_error = logical_restriction.check_restrictions({"age": 25})
    assert validation_error.type == "OR"
    assert (
        validation_error.children[0].message
        == "Age restriction not met, requires exactly 30 years"
    )


# Test for PromoCode check_restrictions method


def test_promocode_check_restrictions():
    promo = PromoCode(
        name="SpecialOffer",
        avantage=Avantage(avantage_type="percent", value=20),
        restrictions=[AgeRestriction(eq=25)],
    )
    # Test with matching age
    assert promo.check_restrictions({"age": 25}) is None

    # Test with non-matching age
    assert (
        promo.check_restrictions({"age": 24}).children[0].message
        == "Age restriction not met, requires exactly 25 years"
    )
