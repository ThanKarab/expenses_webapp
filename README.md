# Expenses Web App
## Tech used: Python, Flask, SqlAlchemy, Sqlite3

### Installation

1. Install `python3`.

1. Install poetry as package manager from [here](https://python-poetry.org/docs/).

1. Install dependencies with poetry in a venv with `poetry install`

1. Start the flask server with:
    ```
   export PYTHONPATH="$PWD" && poetry run python expensesapp/app.py 
   ```

1. (Optional) Run the tests
    ```
   poetry run pytest 
   ```


### Explanation
The app is divided into 3 layers.
1. The models layer is responsible for the database models stored into sqlite3.
2. The service layer is doing most of the work:
   1. It includes its own models used for validation and serialization.
   1. There are `Transaction` child classes for every transaction type.
   1. It has a `transaction_factory` responsible for converting to the proper `Transaction` child class.
   1. It has a _load and _save method to convert to and from DB models.
3. The controller (app) layer is used for the presentation and also parses the csv files.


### Things that could be added
1. Write more tests. Unit/E2E
1. Add logging.
1. Documentation on the methods
1. Add flask error handlers and blueprints
1. Optimization
1. Chunks on the csv input file.
