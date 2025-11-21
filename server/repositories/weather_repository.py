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
        if not self._is_valid_doc(doc):
            logger.warning("Insert called without a valid document.")
            return None

        try:
            collection = await get_collection(self.collection_name)
            city, date = doc.get("city"), doc.get("date")

            if await self._doc_exists(collection, city, date):
                logger.info(f"Weather data for city '{city}' and date '{date}' already exists in the database.")
                existing = await collection.find_one({"city": city, "date": date})
                return existing.get("_id") if existing else None

            result = await collection.insert_one(doc)
            logger.info(f"Inserted new weather data for city '{city}' and date '{date}'.")
            return result.inserted_id

        except DuplicateKeyError:
            self._handle_duplicate_key(doc)
        except (ConnectionFailure, ServerSelectionTimeoutError):
            logger.error("MongoDB connection failed.")
        except OperationFailure as e:
            logger.error(f"MongoDB operation failed: {e}")
        except PyMongoError as e:
            logger.error(f"Unexpected PyMongo error: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error during insert: {e}")

        return None

    def _is_valid_doc(self, doc):
        return doc and isinstance(doc, dict)

    async def _doc_exists(self, collection, city, date):
        if city and date:
            existing = await collection.find_one({"city": city, "date": date})
            return existing is not None
        return False

    def _handle_duplicate_key(self, doc):
        city = doc.get("city") if isinstance(doc, dict) else None
        date = doc.get("date") if isinstance(doc, dict) else None
        if city and date:
            logger.info(f"Duplicate detected: weather data for city '{city}' and date '{date}' already exists.")
        else:
            logger.warning("Duplicate key error while inserting document (missing or invalid doc).")

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
