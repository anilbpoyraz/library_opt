import os
import secrets
from typing import List, Union

from dotenv import load_dotenv
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ Setting class of application """
    load_dotenv()
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 365

    BACKEND_CORS_ORIGINS: Union[str, List[str]] = os.environ.get('BACKEND_CORS_ORIGINS')
    PROJECT_NAME: str = os.environ.get('PROJECT_NAME')
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('SQLALCHEMY_DATABASE_URI')
    HASH_ALGORITHM: str = os.environ.get('HASH_ALGORITHM')

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

settings = Settings()