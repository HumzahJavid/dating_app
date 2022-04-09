import pytest
from fastapi.testclient import TestClient

from dating_app.main import app

# https://fastapi.tiangolo.com/tutorial/testing/
# https://www.starlette.io/testclient/
# https://fastapi.tiangolo.com/advanced/using-request-directly/


@pytest.fixture
def client():
    """Creates a stateless FastAPI test_client

    :yields: A FastAPI Test Client
    """

    with TestClient(app) as client:
        yield client


def test_add():
    example = 32 + 32
    assert example == 64


def test_root_webpage_served_correctly(client):
    """
    Test if server serves root webpage
    """

    response = client.get("/")
    assert response.template.name == "index.html"
    assert "request" in response.context
    assert response.status_code == 200
