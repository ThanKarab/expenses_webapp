import pytest

from expensesapp.models import Transaction
from expensesapp.services import save_transactions


def create_expense_sample_dict():
    return {
        "date": "2022-07-01",
        "type": "Expense",
        "amount": 10.2,
        "memo": "sample_address",
    }


def test_save_transaction_type_not_provided():
    trans = create_expense_sample_dict()
    del trans["type"]
    with pytest.raises(KeyError, match=".* not provided."):
        save_transactions([trans])


def test_save_transaction_type_non_existing():
    trans = create_expense_sample_dict()
    trans["type"] = "non_existing_type"
    with pytest.raises(ValueError, match=".* not a valid TransactionType"):
        save_transactions([trans])


def test_save_transaction_amount_not_provided():
    trans = create_expense_sample_dict()
    del trans["amount"]
    with pytest.raises(ValueError, match=".* field required .*"):
        save_transactions([trans])


def test_save_transaction_amount_is_string():
    trans = create_expense_sample_dict()
    trans["amount"] = "sample_amount"
    with pytest.raises(ValueError, match=".* is not a valid float .*"):
        save_transactions([trans])


def test_save_transaction_date_not_included():
    trans = create_expense_sample_dict()
    del trans["date"]
    with pytest.raises(ValueError, match=".* field required .*"):
        save_transactions([trans])


def test_save_transaction_date_wrong_format():
    trans = create_expense_sample_dict()
    trans["date"] = "22-20-21"
    with pytest.raises(ValueError, match=".* invalid date format .*"):
        save_transactions([trans])


def test_save_transaction_memo_not_included():
    trans = create_expense_sample_dict()
    del trans["memo"]
    with pytest.raises(ValueError, match=".* field required .*"):
        save_transactions([trans])


def test_save_transactions_success(setup_db):
    app, db = setup_db

    trans_dicts = []
    for i in range(3):
        trans_dicts.append(create_expense_sample_dict())

    with app.app_context():
        save_transactions(trans_dicts)

        db_trans = Transaction.query.all()
        assert len(db_trans) == 3
        assert db_trans[0].date == trans_dicts[0]["date"]
        assert db_trans[0].type == trans_dicts[0]["type"]
        assert db_trans[0].amount == trans_dicts[0]["amount"]
        assert db_trans[0].memo == trans_dicts[0]["memo"]

