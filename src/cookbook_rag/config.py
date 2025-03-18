import os
from functools import lru_cache

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """Base class for configs. Thanks for the modification above - if we set
    the `DOTENV_FILE` environment variable, we can use it to load the
    rest of the environment variables from the file. This is useful for
    testing and development, where we might want to use a different
    environment file than the default `.env` file.
    """
    model_config = SettingsConfigDict(
        env_file=find_dotenv(os.getenv("DOTENV_FILE", ".env")),
        extra="ignore",
    )

class QdrantConfig(BaseConfig):
    qdrant_url: str
    qdrant_port: int
    qdrant_index_name: str

class OpenAIConfig(BaseConfig):
    openai_api_key: str

class UnstructuredConfig(BaseConfig):
    unstructured_api_key: str
    unstructured_server_url: str = "https://api.unstructured.io"


@lru_cache
def get_qdrant_config():
    return QdrantConfig()


@lru_cache
def get_openai_config():
    return OpenAIConfig()

@lru_cache
def get_unstructured_config():
    return UnstructuredConfig()
