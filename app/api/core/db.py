import motor.motor_asyncio
from beanie import Document, init_beanie
from typing import Type, TypeVar, List, Optional
import os

# Generic Type for Models
T = TypeVar("T", bound=Document)

DATABASE_URL = os.getenv("MONGO_URI", "mongodb://localhost:27017/swasthasathi")

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client.get_database("swasthasathi")

async def init_db(models: List[Type[Document]]):
    """Initialize the database with Beanie models"""
    await init_beanie(database=db, document_models=models)

class BaseRepository:
    """Generic CRUD operations for Beanie models"""

    @staticmethod
    async def insert_one(model: Type[T], data: dict) -> T:
        """Insert a single document"""
        document = model(**data)
        return await document.insert()

    @staticmethod
    async def insert_many(model: Type[T], data_list: List[dict]) -> List[T]:
        """Insert multiple documents"""
        documents = [model(**data) for data in data_list]
        return await model.insert_many(documents)

    @staticmethod
    async def find_one(model: Type[T], query: dict) -> Optional[T]:
        """Find a single document matching query"""
        return await model.find_one(query)

    @staticmethod
    async def find_many(model: Type[T], query: dict, limit: int = 10) -> List[T]:
        """Find multiple documents matching query"""
        return await model.find(query).limit(limit).to_list()

    @staticmethod
    async def update_one(model: Type[T], query: dict, update_data: dict) -> Optional[T]:
        """Update a single document"""
        document = await model.find_one(query)
        if document:
            await document.set(update_data)
            return document
        return None

    @staticmethod
    async def delete_one(model: Type[T], query: dict) -> bool:
        """Delete a single document"""
        document = await model.find_one(query)
        if document:
            await document.delete()
            return True
        return False
