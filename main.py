from flask import Flask
from mongoengine import connect
from flask import request
import os
from app.services.promotion_service import apply_promotion, create_promotion

mongo_user = os.getenv('MONGO_USER', 'default_user')
mongo_password = os.getenv('MONGO_PASSWORD', 'default_password')
mongo_db_name = os.getenv('MONGO_DB_NAME', 'default_db')
mongo_host = os.getenv('HOST', 'mongodb')

mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}/{mongo_db_name}"
print(mongo_uri)

connect(mongo_db_name, host=mongo_uri)

app = Flask(__name__)


@app.route("/")
def index():
    return "hello world"


@app.route('/apply_promocode', methods=['POST'])
def apply_promocode():
    data = request.json
    return apply_promotion(data)


@app.route('/create_promocode', methods=['POST'])
def create_promocode():
    data = request.json
    return create_promotion(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
