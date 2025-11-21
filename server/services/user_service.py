import logging
from repositories.user_repository import UserRepository
from models.user import User
from typing import Optional

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    async def sign_up(self, user_id: str, name: str, email: str, password: str) -> Optional[str]:
        try:
            return await self.repo.create_user(user_id, name, email, password)
        except Exception as e:
            logger.error(f"Error in sign_up for '{email}': {e}")
            return None

    async def login(self, email: str, password: str) -> Optional[User]:
        try:
            doc = await self.repo.login(email, password)
            if not doc:
                return None
            return User(
                user_id=doc.get("user_id", ""),
                name=doc.get("name", ""),
                email=doc.get("email", ""),
                password=doc.get("password_hash", ""),
                email_verified=doc.get("email_verified", False),
            )
        except Exception as e:
            logger.error(f"Error in login for '{email}': {e}")
            return None

    async def find_by_email(self, email: str) -> Optional[User]:
        try:
            doc = await self.repo.find_by_email(email)
            if not doc:
                return None
            return User(
                user_id=doc.get("user_id", ""),
                name=doc.get("name", ""),
                email=doc.get("email", ""),
                password=doc.get("password_hash", ""),
                email_verified=doc.get("email_verified", False),
            )
        except Exception as e:
            logger.error(f"Error in find_by_email for '{email}': {e}")
            return None

    async def verify_email(self, user_id: str) -> bool:
        try:
            return await self.repo.verify_email(user_id)
        except Exception as e:
            logger.error(f"Error in verify_email for '{user_id}': {e}")
            return False

