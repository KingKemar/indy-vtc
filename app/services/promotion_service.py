from flask import request, jsonify
from app.models.promotion import PromoCode
from main import app

def check_promocode_restrictions(promocode, arguments):



@app.route('/apply_promocode', methods=['POST'])
def apply_promocode():
    data = request.json
    promo_name = data.get("promocode_name")
    arguments = data.get("arguments")

    if not promo_name or not arguments:
        return jsonify({"error": "Missing promocode_name or arguments"}), 400

    # fetch promocode
    promocode = PromoCode.objects(name=promo_name).first()

    if not promocode:
        return jsonify({"error": "Promo code not found"}), 404

    # restrictions check
    if not check_promocode_restrictions(promocode, arguments):
        return jsonify({"error": "Promo code restrictions not met"}), 403

    # Add logic for applying the promocode here

    return jsonify({
        "promocode_name": promocode.name,
        "status": "accepted",
        "avantage": {promocode.avantage.avantage_type: promocode.avantage.value}
    }), 200
