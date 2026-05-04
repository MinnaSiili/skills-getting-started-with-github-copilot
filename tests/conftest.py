import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

BASE_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(BASE_ACTIVITIES)
    yield
    app_module.activities = copy.deepcopy(BASE_ACTIVITIES)


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client
