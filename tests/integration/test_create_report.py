from expensesapp.models import Transaction
from expensesapp.services import create_report
from expensesapp.services import save_transactions


def save_expense_transaction(db):
    db.session.add(
        Transaction(
            date="2022-07-01",
            type="Expense",
            amount=10,
            memo="sample_address",
        )
    )
    db.session.commit()


def save_income_transaction(db):
    db.session.add(
        Transaction(
            date="2022-07-01",
            type="Income",
            amount=20,
            memo="sample_address",
        )
    )
    db.session.commit()


def test_create_report(setup_db):
    app, db = setup_db

    with app.app_context():
        for i in range(3):
            save_income_transaction(db)
        for i in range(3):
            save_expense_transaction(db)

        rep = create_report()

        assert rep.gross_revenue == 60
        assert rep.expenses == 30
        assert rep.net_revenue == 30

