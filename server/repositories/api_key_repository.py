import logging
from db.mongo_client import get_collection
from models.api_key_info import ApiKeyInfo
from pymongo.errors import PyMongoError, DuplicateKeyError, OperationFailure, ConnectionFailure, ServerSelectionTimeoutError
from typing import Optional

logger = logging.getLogger(__name__)

MONGODB_CONN_FAILED_MSG = "MongoDB connection failed."

class ApiKeyRepository:
    def __init__(self, collection_name="api_keys"):
        self.collection_name = collection_name

    async def ensure_indexes(self):
        try:
            collection = await get_collection(self.collection_name)
            await collection.create_index("value", unique=True, expireAfterSeconds=86400)
        except Exception as e:
            logger.error(f"Failed ensuring indexes for api_keys: {e}")

    async def insert(self, api_key_info: ApiKeyInfo) -> Optional[ApiKeyInfo]:
        from datetime import datetime
        try:
            collection = await get_collection(self.collection_name)
            doc = api_key_info.to_dict()
            if "created_at" in doc:
                if isinstance(doc["created_at"], str):
                    try:
                        doc["created_at"] = datetime.fromisoformat(doc["created_at"])
                    except Exception:
                        from datetime import timezone
                        doc["created_at"] = datetime.now(timezone.utc)
            await collection.insert_one(doc)
            logger.info(f"Inserted API key for user '{api_key_info.user_email}' value '{api_key_info.value}'.")
            return api_key_info
        except DuplicateKeyError:
            logger.warning(f"Duplicate API key for user '{api_key_info.user_email}' and value '{api_key_info.value}'.")
        except (ConnectionFailure, ServerSelectionTimeoutError):
            logger.error(MONGODB_CONN_FAILED_MSG)
        except OperationFailure as e:
            logger.error(f"MongoDB operation failed: {e}")
        except PyMongoError as e:
            logger.error(f"Unexpected PyMongo error: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error during API key insert: {e}")
        return None


    async def get(self, user_email: str) -> Optional[ApiKeyInfo]:
        try:
            from datetime import datetime
            collection = await get_collection(self.collection_name)
            doc = await collection.find_one({"user_email": user_email})
            if doc:
                created_at = doc.get("created_at", "")
                if isinstance(created_at, datetime):
                    created_at = created_at.isoformat()
                return ApiKeyInfo(
                    user_email=doc.get("user_email", ""),
                    value=doc.get("value", ""),
                    created_at=created_at,
                )
            return None
        except (ConnectionFailure, ServerSelectionTimeoutError):
            logger.error(MONGODB_CONN_FAILED_MSG)
        except OperationFailure as e:
            logger.error(f"MongoDB operation failed: {e}")
        except PyMongoError as e:
            logger.error(f"Unexpected PyMongo error: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error during API key get: {e}")
        return None