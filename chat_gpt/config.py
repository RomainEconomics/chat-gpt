import os
from pathlib import Path
import yaml
from pydantic import BaseModel

CONFIG_PATH = Path(os.path.expanduser("~/.config/utils/custom-chat-gpt/config.yml"))


class Config(BaseModel):
    MODEL_NAME: str
    SQLITE_DB: str

    WEAVIATE_HOST: str
    WEAVIATE_PORT: int
    WEAVIATE_GRPC_HOST: str
    WEAVIATE_GRPC_PORT: int


def load_config() -> Config:
    with open(CONFIG_PATH, "r") as file:
        config_data = yaml.safe_load(file)
        config_data = {k.upper(): v for k, v in config_data.items()}
    return Config(**config_data)
