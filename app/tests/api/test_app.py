import json
import pytest
from app.settings.settings import config
from app.tests.api.test_app_constants import RUN_DICT
from app.api.app import app


@pytest.fixture
def client():
    app.config.update(config)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def image_test():
    file = 'app/tests/img/small.png'
    data = {
        'file': (open(file, 'rb'), file),
    }
    return data


@pytest.fixture
def image_run():
    # high quality picture
    file = 'app/tests/img/run.jpeg'
    data = {
        'file': (open(file, 'rb'), file),
    }
    return data


@pytest.fixture
def image_run_strict():
    # picture is not so clear
    file = 'app/tests/img/run_unclear.jpeg'
    data = {
        'threshold': '1',
        'file': (open(file, 'rb'), file),
    }
    return data


@pytest.fixture
def invalid_file():
    # picture is not so clear
    file = 'app/tests/img/file.strange'
    data = {
        'file': (open(file, 'rb'), file),
    }
    return data


def test_basic_endpoint_response(client, image_test):
    response = client.post('api/basic', data=image_test)
    # checks response
    assert response.status_code == 200
    # checks type
    data = response.json['data']
    assert type(data['interpreted']) is list


def test_basic_endpoint_response_run(client, image_run):
    response = client.post('api/basic', data=image_run)
    data = response.json['data']
    # checks response
    assert response.status_code == 200


def test_cni_endpoint_response(client, image_test):
    # image_test is not clear enough so we expect a 415 response
    response = client.post('api/cni', data=image_test)
    # checks response
    assert response.status_code == 415


def test_cni_endpoint_response_run(client, image_run):
    # image_run is not clear enough so we expect a 415 response
    response = client.post('api/cni', data=image_run)
    # checks response
    assert response.status_code == 200
    # checks type
    data = response.json['data']
    assert type(data) is dict
    # checks content
    assert data == RUN_DICT


def test_basic_endpoint_response_run_strict(client, image_run_strict):
    # we test that threshold arg works and that as the threshold is
    # to read perfectly, we expect not to reciecve a correct answer
    response = client.post('api/cni', data=image_run_strict)
    # checks response
    assert response.status_code == 415


def test_invalid_file(client, invalid_file):
    # we test that threshold arg works and that as the threshold is
    # to read perfectly, we expect not to reciecve a correct answer
    response = client.post('api/cni', data=invalid_file)
    # checks response
    assert response.status_code == 415


def test_invalid_service_name(client, image_test):
    # use of unexisting url and its corresponding method
    response = client.post('api/DoesNotAndWillNotExist', data=image_test)
    # checks response
    assert response.status_code == 400
