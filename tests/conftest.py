import pytest
from mongoengine import connect, disconnect
from app.models.promotion import PromoCode
from mongoengine import connect
from main import app

import os


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
def mongodb_connection():
    user = os.getenv('MONGO_USER')
    password = os.getenv('MONGO_PASSWORD')
    db_name = os.getenv('MONGO_DB_NAME')
    host = os.getenv('HOST')
    connect(db_name, host=f'mongodb://{user}:{password}@{host}/{db_name}')
    yield
    disconnect()


@pytest.fixture(autouse=True)
def clean_up():
    yield
    # Cleanup the database after each test
    PromoCode.objects.delete()
