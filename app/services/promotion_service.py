from flask import jsonify
from mongoengine import ValidationError

from app.models.promotion import PromoCode
from app.utils.meteo import get_weather


def apply_promotion(data):
    promo_name = data.get("promocode_name")
    arguments = data.get("arguments")

    if not promo_name or not arguments:
        return jsonify({"error": "Missing promocode_name or arguments"}), 400

    # fetch promocode
    promocode = PromoCode.objects(name=promo_name).first()

    if not promocode:
        return jsonify({"error": "Promo code not found"}), 404

    town_temp, weather_description = get_weather(arguments["meteo"]["town"])

    # porting town weather values in the arguments to make the checks easier.
    arguments["meteo"]["weather"] = weather_description
    arguments["meteo"]["temp"] = town_temp

    # restrictions check
    restrictions_met = promocode.check_restrictions(arguments)
    if restrictions_met:
        return (
            jsonify(
                {
                    "promocode_name": promocode.name,
                    "status": "denied",
                    "reasons": restrictions_met.jsonify(),
                }
            ),
            403,
        )

    # Add logic for applying the promocode here

    return (
        jsonify(
            {
                "promocode_name": promocode.name,
                "status": "accepted",
                "avantage": {
                    promocode.avantage.avantage_type: promocode.avantage.value
                },
            }
        ),
        200,
    )


def create_promotion(data):
    try:
        # Create PromoCode instance from JSON data
        promo = PromoCode.from_json(data)
        promo.clean()  # Validate the promo code
        promo.save()  # Save to database

        return jsonify({"message": "PromoCode created successfully"}), 201

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
