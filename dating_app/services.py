import asyncio

import motor.motor_asyncio
from db.database import MONGODB_URL


def create_database():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

    return client


async def list_dbs(client):
    dbs = await client.list_database_names()
    return dbs


# ---------------- example features / testing purposes


async def main():
    client = create_database()
    default_database = client.get_default_database()
    print(f"default db: {default_database.name}")
    dbs = await list_dbs(client)
    print(dbs)


if __name__ == "__main__":
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    asyncio.run(main())
