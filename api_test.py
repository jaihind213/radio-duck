import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import api
import config
import duck

app = FastAPI()
app.include_router(api.router)

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_before_test():
    config.setup_app_config(os.getcwd() + "/default.ini")
    duck.setup_duck()
    yield

@pytest.fixture(scope="module", autouse=True)
def cleanup_after_test():
    yield
    duck.connection.close()

def test_quack():
    response = client.get("/quack")
    assert response.status_code == 200
    assert 'quack quack. serving you on port' in response.text

def test_run_sql():
    response = client.post("/sql", json= {"sql": "select sum(total) as num_birds_in_pond from pond","timeout": 0})
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    resp_dict = response.json()
    assert len(resp_dict) == 3, "Number of keys in api response json should be 3"
    assert len(resp_dict['columns']) == 1, "Number of columns in response json should be 1"
    assert resp_dict['columns'][0] == 'num_birds_in_pond', "Column name expected in response json should be 'num_birds_in_pond'"
    assert resp_dict['schema'][0] == 'NUMBER', "Column Type expected in response json should be Number"
    assert len(resp_dict['rows']) == 1, "Number of rows expected should be 1"
    assert resp_dict['rows'][0][0] > 1, "Number of birds we selected from pond should be > 1"

def test_run_for_absent_table():
    response = client.post("/sql", json= {"sql": "select * from fubar","timeout": 0})
    assert response.status_code == 400
    assert 'fubar does not exist' in response.json()['detail']

def test_run_for_bad_column():
    response = client.post("/sql", json= {"sql": "select fubar from pond","timeout": 0})
    assert response.status_code == 400
    assert '"fubar" not found' in response.json()['detail']

def test_run_for_bad_query():
    response = client.post("/sql", json= {"sql": "SELECTS * from pond","timeout": 0})
    assert response.status_code == 400

def test_run_with_named_params():
    response = client.post("/sql", json= {"sql": "select count(*) as total from pond where duck_type = ?", "parameters": ['swan'] })
    resp_dict = response.json()
    assert resp_dict['rows'][0][0] == 0, "Number of swans we selected from pond should be 0"
    response = client.post("/sql", json={"sql": "select count(*) as total from pond where duck_type = ?",
                                         "parameters": ['mighty_duck']})
    resp_dict = response.json()
    assert resp_dict['rows'][0][0] > 0, "Number of mighty_ducks we selected from pond should be >0"

    response = client.post("/sql", json={"sql": "select total from pond where duck_type = 'wood_duck'",
                                         "parameters": ['no_qns_mark_in_query_but_sending_param']})
    assert response.status_code == 400 # InvalidInputException('Invalid Input Error: Prepared statement needs 0 parameters, 1 given')