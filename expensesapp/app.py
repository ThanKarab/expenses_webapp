import os

from flask import Flask
from flask import request

from expensesapp.models import db
from expensesapp.services import create_report
from expensesapp.services import save_transactions

app = Flask(__name__)
app.config["DEBUG"] = True
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

UPLOADED_FILE_NAME = "data"


@app.route("/transactions", methods=["POST"])
def post_transactions():
    if not request.files:
        return "The request should contain a file.", 400

    if UPLOADED_FILE_NAME not in request.files:
        return f"The request should contain a file named '{UPLOADED_FILE_NAME}'.", 400

    try:
        uploaded_file = request.files[UPLOADED_FILE_NAME].read().decode("ascii")
        trans_dicts = _parse_transactions_csv(uploaded_file)

        save_transactions(trans_dicts)
    except Exception as exc:
        return str(exc), 400

    return ""


def _parse_transactions_csv(csv):
    transactions = []
    for line in csv.split("\n"):
        # Skip empty lines
        if not line:
            continue

        # Skip commented lines
        if line.lstrip().startswith("#"):
            continue

        values = line.split(",")
        stripped_values = [value.strip() for value in values]
        trans_dict = {
            "date": stripped_values[0],
            "type": stripped_values[1],
            "amount": stripped_values[2],
            "memo": stripped_values[3],
        }
        transactions.append(trans_dict)
    return transactions


@app.route("/report")
def get_report():
    return create_report().json()


if __name__ == "__main__":
    app.run()
