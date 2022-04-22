import asyncio

from db.database import MONGODB_URL
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.User import UserCreate


# return a session
async def get_db():
    s = await client.start_session()
    try:
        yield s
    finally:
        await s.end_session()


async def insert_and_display_test_data(client):
    default_db = client.get_default_database()

    collection_name = default_db["collection_test"]
    test_doc = {"key_1": "Test field in test doc", "key_2": 42}
    result = await collection_name.insert_one(test_doc)
    print(result.inserted_id)

    # display data
    docs_cursor = collection_name.find()
    # must specify list length (can be larger than actual number of collections)
    # result = await docs_cursor.to_list(100)
    # print(result)

    # https://motor.readthedocs.io/en/stable/api-asyncio/cursors.html#asynciomotorcommandcursor
    async for doc in docs_cursor:
        print(doc)


async def create_user(db, user: UserCreate):
    user = jsonable_encoder(user)
    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    print(f"Created user is {created_user}")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


# ---------------- example features / testing purposes
if __name__ == "__main__":
    client = AsyncIOMotorClient(MONGODB_URL)
    asyncio.run(insert_and_display_test_data(client))
