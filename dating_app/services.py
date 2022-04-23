import asyncio

from db.database import MONGODB_URL
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.User import RegisterResponse, UserCreate


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


async def create_user(db, user: UserCreate) -> RegisterResponse:
    user_json = jsonable_encoder(user)
    db_user = await db["users"].find_one({"email": user_json["email"]})

    if db_user:
        # # This exception is blocking
        # raise HTTPException(status_code=409, detail="Email already in use")
        return RegisterResponse(
            message="Email already in use.", email=user_json["email"]
        )

    new_user = await db["users"].insert_one(user_json)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return RegisterResponse(
        message="Created user with email.", email=created_user["email"]
    )


# ---------------- example features / testing purposes
if __name__ == "__main__":
    client = AsyncIOMotorClient(MONGODB_URL)
    asyncio.run(insert_and_display_test_data(client))
