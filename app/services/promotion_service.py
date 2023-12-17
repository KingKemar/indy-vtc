from flask import request, jsonify
from app.models.promotion import PromoCode
from app.utils.meteo import get_weather


def apply_promotion(data):
    promo_name = data.get("promocode_name")
    arguments = data.get("arguments")

    print(arguments)
    print(promo_name)

    if not promo_name or not arguments:
        return jsonify({"error": "Missing promocode_name or arguments"}), 400

    # fetch promocode
    promocode = PromoCode.objects(name=promo_name).first()

    if not promocode:
        return jsonify({"error": "Promo code not found"}), 404

    town_temp, weather_description = get_weather(arguments['meteo']['town'])

    # porting town weather values in the arguments to make the checks easier.
    arguments['meteo']['weather'] = weather_description
    arguments['meteo']['temp'] = town_temp

    # restrictions check
    restrictions_met, error_list = promocode.check_restrictions(arguments)
    if not restrictions_met:
        return jsonify({
            "promocode_name": promocode.name,
            "status": "denied",
            "reasons": {
                error_list
            }
        }), 403

    # Add logic for applying the promocode here

    return jsonify({
        "promocode_name": promocode.name,
        "status": "accepted",
        "avantage": {promocode.avantage.avantage_type: promocode.avantage.value}
    }), 200
