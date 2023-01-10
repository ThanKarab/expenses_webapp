import os

import requests

from tests.e2e import report_url
from tests.e2e import transactions_url

basedir = os.path.abspath(os.path.dirname(__file__))


def test_post_transactions():
    files = {'data': open(basedir + '/data.csv', 'rb')}
    response = requests.post(transactions_url, files=files)
    assert response.status_code == 200


def test_post_transactions_error():
    files = {'data': open(basedir + '/bad_type.csv', 'rb')}
    response = requests.post(transactions_url, files=files)
    assert response.status_code == 400
    assert "'non_existing' is not a valid" in response.text


def test_create_report():
    response = requests.get(report_url)
    assert response.status_code == 200

    res_json = response.json()
    assert "gross_revenue" in res_json.keys()
    assert "expenses" in res_json.keys()
    assert "net_revenue" in res_json.keys()
    assert res_json["gross_revenue"] > 0
    assert res_json["expenses"] > 0
    assert res_json["net_revenue"] > 0

