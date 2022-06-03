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


async def test_insert_and_display_test_data(client):
    default_db = client.get_default_database()

    collection_name = default_db["collection_test"]
    test_doc = {"key_1": "Test field in test doc", "key_2": 42}
    result = await collection_name.insert_one(test_doc)
    print(result.inserted_id)

    # display data
    docs_cursor = collection_name.find()
    async for doc in docs_cursor:
        print(doc)
