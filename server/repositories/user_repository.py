import logging
import os
import base64
import hashlib
from typing import Optional, Dict, Any
from db.mongo_client import get_collection
from pymongo.errors import PyMongoError, DuplicateKeyError, OperationFailure, ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, collection_name: str = "users"):
        self.collection_name = collection_name

    async def _get_collection(self):
        return await get_collection(self.collection_name)

    def _hash_password(self, password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
        if salt is None:
            salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
        return {"salt": base64.b64encode(salt).decode(), "hash": base64.b64encode(hashed).decode()}

    async def create_user(self, user_id: str, name: str, email: str, password: str) -> Optional[str]:
        try:
            coll = await self._get_collection()
            existing = await coll.find_one({"email": email})
            if existing:
                logger.info(f"User with email '{email}' already exists.")
                return str(existing.get("_id"))
            ph = self._hash_password(password)
            doc = {
                "user_id": user_id,
                "name": name,
                "email": email,
                "password_hash": ph["hash"],
                "password_salt": ph["salt"],
                "email_verified": False,
            }
            result = await coll.insert_one(doc)
            return str(result.inserted_id)
        except DuplicateKeyError:
            logger.warning(f"Duplicate key while creating user '{email}'.")
        except (ConnectionFailure, ServerSelectionTimeoutError):
            logger.error("MongoDB connection failed.")
        except OperationFailure as e:
            logger.error(f"MongoDB operation failed: {e}")
        except PyMongoError as e:
            logger.error(f"Unexpected PyMongo error: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error creating user: {e}")
        return None

    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        try:
            coll = await self._get_collection()
            return await coll.find_one({"email": email})
        except Exception as e:
            logger.error(f"Error finding user by email '{email}': {e}")
            return None

    async def verify_email(self, user_id: str) -> bool:
        try:
            coll = await self._get_collection()
            result = await coll.update_one({"user_id": user_id}, {"$set": {"email_verified": True}})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error verifying email for user '{user_id}': {e}")
            return False

    async def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        try:
            coll = await self._get_collection()
            doc = await coll.find_one({"email": email})
            if not doc:
                return None
            salt_b = base64.b64decode(doc.get("password_salt", ""))
            test_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_b, 100_000)
            if base64.b64encode(test_hash).decode() == doc.get("password_hash"):
                return doc
            return None
        except Exception as e:
            logger.error(f"Login error for '{email}': {e}")
            return None
