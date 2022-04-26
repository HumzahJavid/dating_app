from fastapi.encoders import jsonable_encoder

from dating_app.schemas.User import (
    LoginResponse200,
    LoginResponse401,
    RegisterResponse,
    UserCreate,
    UserModel,
    UserSearch,
)


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


async def authenticate_user(db, user: UserModel):
    user_json = jsonable_encoder(user)

    db_user = await db["users"].find_one({"email": user_json["email"]})

    if not db_user:
        return LoginResponse401()

    password_match = user_json["password"] == db_user["password"]

    if not password_match:
        return LoginResponse401()

    db["users"].update_one({"email": user_json["email"]}, {"$set": {"is_active": True}})
    return LoginResponse200()


async def get_current_user(db):
    user = await db["users"].find_one({"is_active": True})
    if not user:
        print("Active User not found")

    return user


async def logout(db):
    user = await get_current_user(db)
    if not user:
        return {"message": "500 no active users to logout"}

    db["users"].update_one({"email": user["email"]}, {"$set": {"is_active": False}})
    return {"message": "Logged out"}


async def list_users(db):
    users = []
    # find all users except the logged in user
    users_cursor = db["users"].find({"is_active": {"$nin": [True]}})
    async for user in users_cursor:
        users.append(user)
    return users


async def search_users(db, search: UserSearch):
    search_results = []
    search_json = jsonable_encoder(search)
    print(search_json)
    name = search_json["name"]
    email = search_json["email"]
    min_age = search_json["min_age"]
    max_age = search_json["max_age"]
    search_type = mongo_logical_operator(search_json["search_type"])
    gender = search_json["gender"]

    print(f"name = {name}")
    print(f"email = {email}")
    print(f"min age = {min_age}")
    print(f"max age = {max_age}")
    print(f"gender = {gender}")

    if email:
        # conduct a single search result
        print(f"found email {email}, returning single result")
        user = await db["users"].find_one({"email": search_json["email"]})
        search_results.append(user)
        return search_results
    else:
        print("no email found...")
        # conduct an 'and/or' search operation
        criteria = [
            {"name": {"$eq": name}},
            {"age": {"$gt": min_age, "$lt": max_age}},
            {"gender": {"$eq": gender}},
        ]
        search_criteria = {search_type: criteria}
        print(f"searching with search criteria {search_criteria}")
        users = db["users"].find(search_criteria)

        async for user in users:
            search_results.append(user)
            print(user)

    return search_results


def mongo_logical_operator(operator):
    """
    Converts logical operators 'and' / 'or' string to mongo compatible operators
    by prepending a '$' sign i.e. 'and' -> '$and'
    """

    if isinstance(operator, str):
        if "$" not in operator:
            print(f"coverting '{operator}' to mongo operator")
            return "$" + operator
        return operator
