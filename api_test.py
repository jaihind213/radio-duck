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
    print("xxxxx")
    duck.connection.close()

def test_quack():
    response = client.get("/quack")
    assert response.status_code == 200
    assert 'quack quack. serving you on port' in response.json()

def test_run_sql():
    response = client.post("/sql", json= {"sql": "select sum(total) as num_birds_in_pond from pond","timeout": 0})
    assert response.status_code == 200
    resp_dict = response.json()
    assert len(resp_dict) == 3
    assert len(resp_dict['columns']) == 1
    assert resp_dict['columns'][0] == 'num_birds_in_pond'
    assert resp_dict['schema'][0] == 'NUMBER'
    assert len(resp_dict['rows']) == 1
    assert resp_dict['rows'][0][0] > 1
