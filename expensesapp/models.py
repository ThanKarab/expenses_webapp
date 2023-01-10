import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float
from sqlalchemy import String

db = SQLAlchemy()

TRANSACTIONS = "transactions"


def create_uuid():
    return str(uuid.uuid4())


class Transaction(db.Model):
    __tablename__ = TRANSACTIONS
    id = db.Column(String(36), primary_key=True, default=create_uuid, unique=True)
    date = db.Column(String(20), nullable=False)
    type = db.Column(String(20), nullable=False)
    amount = db.Column(Float(), nullable=False)
    memo = db.Column(String(50), nullable=False)
