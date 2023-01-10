from abc import ABC
from abc import abstractmethod
from datetime import date as dt_date
from enum import Enum
from typing import List

from pydantic import BaseModel
from pydantic import Field

from expensesapp.models import db
from expensesapp.models import Transaction as DB_Transaction


class TransactionType(Enum):
    EXPENSE = "Expense"
    INCOME = "Income"


class Transaction(BaseModel, ABC):
    date: dt_date
    type: TransactionType
    amount: float
    memo: str

    class Config:
        allow_mutation = False

    @property
    @abstractmethod
    def revenue(self):
        raise NotImplemented()

    @property
    @abstractmethod
    def expenses(self):
        raise NotImplemented()


class Expense(Transaction):
    type = TransactionType.EXPENSE

    @property
    def expense_category(self):
        return self.memo

    @property
    def revenue(self):
        return 0

    @property
    def expenses(self):
        return self.amount


class Income(Transaction):
    type = TransactionType.INCOME

    @property
    def job_address(self):
        return self.memo

    @property
    def revenue(self):
        return self.amount

    @property
    def expenses(self):
        return 0


def transaction_factory(trans_dict):
    type_key = "type"

    if type_key not in trans_dict.keys():
        raise KeyError(f"The '{type_key}' of the transaction is not provided.")

    tr_type = TransactionType(trans_dict[type_key])
    if tr_type == TransactionType.INCOME:
        return Income.parse_obj(trans_dict)
    elif tr_type == TransactionType.EXPENSE:
        return Expense.parse_obj(trans_dict)
    else:
        raise ValueError(f"The '{str(tr_type)}' transaction type is not supported.")


class Report(BaseModel):
    gross_revenue: float = Field(alias="gross-revenue", default=0)
    expenses: float = Field(default=0)
    net_revenue: float = Field(alias="net-revenue", default=0)

    def include_transaction(self, tr: Transaction):
        self.gross_revenue += tr.revenue
        self.expenses += tr.expenses
        self.net_revenue = self.gross_revenue - self.expenses


def save_transactions(trans_dicts: List[dict]):
    for trans_dict in trans_dicts:
        trans = transaction_factory(trans_dict)
        _save_transaction(trans)
    db.session.commit()


def create_report():
    rep = Report()
    for db_trans in DB_Transaction.query.all():
        trans = _load_transaction(db_trans)
        rep.include_transaction(trans)
    return rep


def _save_transaction(trans: Transaction):
    db_trans = DB_Transaction(
        date=str(trans.date),
        type=trans.type.value,
        amount=trans.amount,
        memo=trans.memo,
    )
    db.session.add(db_trans)


def _load_transaction(trans: DB_Transaction) -> Transaction:
    trans_dict = {
        "date": trans.date,
        "type": trans.type,
        "amount": trans.amount,
        "memo": trans.memo,
    }
    return transaction_factory(trans_dict)
