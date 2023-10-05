from pydantic_settings import BaseSettings
from pydantic import BaseModel
from functools import lru_cache
import json

CONFIG = 'env.json'

@lru_cache()
def to_config():
    with open(CONFIG, 'r') as f:
        return Config(**json.loads(f.read()))

def set_config(**kwargs):
    with open(CONFIG, 'w') as f:
        f.write(json.dumps(kwargs)) 

class Ports(BaseModel):
    client: int
    api: int

class Config(BaseSettings):
    ports: Ports

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
