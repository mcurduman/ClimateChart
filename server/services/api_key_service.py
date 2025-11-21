import logging
import time
import os
import base64
from typing import Optional
from repositories.api_key_repository import ApiKeyRepository
from models.api_key_info import ApiKeyInfo

logger = logging.getLogger(__name__)

ISO_FMT = "%Y-%m-%dT%H:%M:%SZ"

class ApiKeyService:
	def __init__(self):
		self.repo = ApiKeyRepository()

	async def init(self):
		logger.info("Initializing ApiKeyService and ensuring indexes.")
		await self.repo.ensure_indexes()

	def _generate_key(self, length: int = 32) -> str:
		return base64.urlsafe_b64encode(os.urandom(length)).decode().rstrip("=")

	async def create_key(self, user_email: str) -> Optional[ApiKeyInfo]:
		user_email = (user_email or "").strip().lower()
		if not user_email:
			logger.warning("create_key called without user_email")
			return None
		value = self._generate_key()
		created_at = time.strftime(ISO_FMT, time.gmtime(time.time()))
		info = ApiKeyInfo(
			user_email=user_email,
			value=value,
			created_at=created_at,
		)
		result = await self.repo.insert(info)
		return result

	async def get_key(self, user_email: str) -> Optional[ApiKeyInfo]:
		user_email = (user_email or "").strip().lower()
		if not user_email:
			return None
		return await self.repo.get(user_email)