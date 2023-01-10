import os

import pytest
from flask import Flask

from expensesapp.models import db

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture(scope="function")
def setup_db():
    app = Flask(__name__)
    app.config.update(
        DEBUG=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'db.sqlite3'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

    return app, db
