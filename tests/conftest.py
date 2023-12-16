import pytest
from mongoengine import connect, disconnect
from app.models.promotion import PromoCode
from mongoengine import connect

import os


@pytest.fixture(scope='session', autouse=True)
def mongodb_connection():
    user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    db_name = os.getenv('MONGO_DB_NAME')
    host = os.getenv('HOST')
    print(f'mongodb://{user}:{password}@{host}/{db_name}')
    connect(db_name, host=f'mongodb://{user}:{password}@{host}/{db_name}')
    yield
    disconnect()


@pytest.fixture(autouse=True)
def clean_up():
    yield
    # Cleanup the database after each test
    PromoCode.objects.delete()
