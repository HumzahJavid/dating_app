"""
Test file to connect to the local mongo db instance and print out version info.
"""
import asyncio

import motor.motor_asyncio

MONGODB_URL = "mongodb://localhost:27017"


async def get_server_info():

    # set a 5-second connection timeout
    client = motor.motor_asyncio.AsyncIOMotorClient(
        MONGODB_URL, serverSelectionTimeoutMS=5000
    )

    try:
        print(await client.server_info())
    except Exception:
        print("Unable to connect to the server.")


loop = asyncio.get_event_loop()
loop.run_until_complete(get_server_info())
