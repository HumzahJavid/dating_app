from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB:
    MONGODB_URL = "mongodb://localhost:27017/dating_app"

    def __init__(self):
        self.mongodb_client = None
        self.mongodb = None

    async def startup_db_client(self) -> None:
        self.mongodb_client = AsyncIOMotorClient(self.MONGODB_URL)
        self.mongodb = self.mongodb_client.get_default_database()

    async def shutdown_db_client(self) -> None:
        self.mongodb_client.close()
        self.mongodb = None
