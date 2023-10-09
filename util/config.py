from pydantic import BaseSettings
from pydantic import BaseModel
from functools import lru_cache
from typing import Dict, List
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

class Game(BaseModel):
    id: int
    name: str
    generation: int
    dexes: Dict[int, str]
    regions: Dict[int, str]

class Config(BaseSettings):
    dex_dict: Dict[int, str]
    gen_dict: Dict[int, List[Game]]
    three_grams: Dict[str, List[int]]
    two_grams: Dict[str, List[int]]
    one_grams: Dict[str, List[int]]
    api_url: str
    ports: Ports
    ndex: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
