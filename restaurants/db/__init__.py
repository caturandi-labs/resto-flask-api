from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()
ma = Marshmallow()

def init_db(app):
    """ Initialize the database. """
    db.init_app(app)
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        if not existing_tables:
            db.create_all()
    return db

def init_ma(app):
    ma.init_app(app)
    return ma