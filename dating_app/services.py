from fastapi.encoders import jsonable_encoder

from dating_app.schemas.User import (
    LoginResponse200,
    LoginResponse401,
    RegisterResponse,
    UserCreate,
    UserModel,
    UserSearch,
)


async def create_user(db, user: UserCreate) -> RegisterResponse:
    user_json = jsonable_encoder(user)
    db_user = await db["users"].find_one({"email": user_json["email"]})

    if db_user:
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
    return LoginResponse200(email=user_json["email"])


async def get_current_user(db):
    """Returns the current user"""

    # Have not updated method for multi user (using mongodbsession instances)
    # Works in some cases not users
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
    """Return all other users except the logged in one"""

    current_user = await get_current_user(db)
    print("current users email = ")
    email = current_user["email"]
    print(email)
    users = []
    users_cursor = db["users"].find({"email": {"$not": {"$eq": email}}})
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
        criteria = [{"age": {"$gt": min_age, "$lt": max_age}}]

        if name:
            criteria.append({"name": {"$eq": name}})
        if gender:
            criteria.append({"gender": {"$eq": gender}})
        search_criteria = {search_type: criteria}
        print(f"searching with search criteria {search_criteria}")
        users = db["users"].find(search_criteria)

        async for user in users:
            search_results.append(user)
            print(user)

    return search_results


async def update_user(db, current_user, user_to_update):
    update_id = current_user["_id"]
    print("updating user id ", update_id)
    update_result = await db["users"].update_one(
        {"_id": update_id}, {"$set": user_to_update}
    )

    if update_result.modified_count == 1:
        return {"success:200"}
    else:
        return {"result ": update_result.raw_result}


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
