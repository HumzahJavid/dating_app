import asyncio

import motor.motor_asyncio
from db.database import MONGODB_URL


def create_database():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

    return client


async def insert_and_display_test_data(client):
    default_db = client.get_default_database()

    collection_name = default_db["collection_test"]
    test_doc = {"key_1": "Test field in test doc", "key_2": 42}
    result = await collection_name.insert_one(test_doc)
    print(result.inserted_id)


# ---------------- example features / testing purposes


async def main():
    client = create_database()
    await insert_and_display_test_data(client)


if __name__ == "__main__":
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    asyncio.run(main())
