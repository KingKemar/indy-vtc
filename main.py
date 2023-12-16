from flask import Flask
from mongoengine import connect

import os

mongo_user = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'default_user')
mongo_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'default_password')
mongo_db_name = os.getenv('MONGO_DB_NAME', 'default_db')
mongo_host = 'mongodb'

mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}/{mongo_db_name}"
print(mongo_uri)

connect(mongo_db_name, host=mongo_uri)

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)
