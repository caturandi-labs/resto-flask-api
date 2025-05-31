import pytest
import sys
import os

from app import app, db

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['FLASK_ENV'] = "testing"
os.environ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"

@pytest.fixture
def test_app():
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()
