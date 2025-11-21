import logging
from db.mongo_client import get_collection
from pymongo.errors import PyMongoError, DuplicateKeyError, OperationFailure, ConnectionFailure, ServerSelectionTimeoutError
from datetime import timezone

logger = logging.getLogger(__name__)




class EmailRepository:
    def __init__(self, collection_name="email_verifications"):
        self.collection_name = collection_name

    async def ensure_ttl_index(self):
        try:
            collection = await get_collection(self.collection_name)
            await collection.create_index("created_at", expireAfterSeconds=900)
            logger.info("TTL index created for email_verifications (15 min)")
        except Exception as e:
            logger.error(f"Failed to create TTL index for email_verifications: {e}")

    async def insert_verification(self, user_email: str, code: str):
        from datetime import datetime
        try:
            collection = await get_collection(self.collection_name)
            created_at = datetime.now(timezone.utc)
            doc = {"user_email": user_email, "code": code, "created_at": created_at}
            await collection.insert_one(doc)
            logger.info(f"Inserted verification code for user '{user_email}'.")
            return doc
        except DuplicateKeyError:
            logger.warning(f"Duplicate verification for user '{user_email}'.")
        except (ConnectionFailure, ServerSelectionTimeoutError):
            logger.error("MongoDB connection failed.")
        except OperationFailure as e:
            logger.error(f"MongoDB operation failed: {e}")
        except PyMongoError as e:
            logger.error(f"Unexpected PyMongo error: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error during verification insert: {e}")
        return None

    async def get_by_user_email(self, user_email: str):
        try:
            collection = await get_collection(self.collection_name)
            doc = await collection.find_one({"user_email": user_email})
            return doc
        except (ConnectionFailure, ServerSelectionTimeoutError):
            logger.error("MongoDB connection failed.")
        except OperationFailure as e:
            logger.error(f"MongoDB operation failed: {e}")
        except PyMongoError as e:
            logger.error(f"Unexpected PyMongo error: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error during verification get: {e}")
        return None
