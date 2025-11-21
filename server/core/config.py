from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from enum import Enum

class Env(str, Enum):
	development = "development"
	production = "production"

class Settings(BaseSettings):
	ENV: Env = Env.development
	APP_NAME: str
	API_KEY_HEADER: str
	AUTHZ_HEADER: str
	EXPECTED_API_KEY: str
	PUBLIC_METHODS: str = ""
	API_KEY_METHODS: str = ""
	DB_URL: str
	API_URL: str

	DEFAULT_SENDER: str
	PASSWORD: str
	TEMPLATE_UUID: str

	model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")
	
	def __init__(self, **values):
		super().__init__(**values)
		self.PUBLIC_METHODS = {m.strip() for m in self.PUBLIC_METHODS.split(",") if m.strip()}
		self.API_KEY_METHODS = {m.strip() for m in self.API_KEY_METHODS.split(",") if m.strip()}

@lru_cache
def get_settings() -> Settings:
	return Settings()
