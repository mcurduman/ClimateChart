import logging
from db.mongo_client import get_collection
from pymongo.errors import (
    PyMongoError, ServerSelectionTimeoutError, DuplicateKeyError,
    OperationFailure, ConnectionFailure, ExecutionTimeout)

logger = logging.getLogger(__name__)

class WeatherRepository:
    def __init__(self, collection_name="weather"):
        self.collection_name = collection_name

    async def insert(self, doc):
        try:
            collection = await get_collection(self.collection_name)
            result = await collection.insert_one(doc)
            return result.inserted_id

        except DuplicateKeyError:
            logger.warning("Duplicate key error while inserting document.")
        except (ConnectionFailure, ServerSelectionTimeoutError):
            logger.error("MongoDB connection failed.")
        except OperationFailure as e:
            logger.error(f"MongoDB operation failed: {e}")
        except PyMongoError as e:
            logger.error(f"Unexpected PyMongo error: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error during insert: {e}")

        return None

    async def find(self, query=None):
        if query is None:
            query = {}

        try:
            collection = await get_collection(self.collection_name)
            cursor = collection.find(query)
            return [doc async for doc in cursor]

        except ExecutionTimeout:
            logger.warning("Query execution timeout.")
        except (ConnectionFailure, ServerSelectionTimeoutError):
            logger.error("MongoDB connection failed during find.")
        except PyMongoError as e:
            logger.error(f"PyMongoError during find: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error during find: {e}")

        return []
