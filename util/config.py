from pydantic import BaseSettings
from pydantic import BaseModel
from functools import lru_cache
from typing import Dict, List
import json

CONFIG = 'env.json'

def parse_generations(games):
    gen_dict = dict()
    all_gen_ids = set([
       game['generation'] for game in games.values() 
    ])
    gen_dexes = {
        gen: [
            game for (gid, game) in games.items()
            if gen == game['generation']
        ]
        for gen in list(all_gen_ids)
    }
    return gen_dexes

def to_ngrams(dex_dict):
    three_grams = dict()
    for dexn,name in dex_dict.items():
        dex_list = three_grams.get(name[:3], [])
        three_grams[name[:3]] = dex_list + [dexn]

    two_grams = dict()
    for k, v in three_grams.items():
        two_list = two_grams.get(k[:2], [])
        two_grams[k[:2]] = two_list + v

    return (three_grams, two_grams)

@lru_cache()
def to_config():
    with open(CONFIG, 'r') as f:
        kwargs = json.loads(f.read())
        gen_dict = parse_generations(
            kwargs['game_dict']
        )
        (three_grams, two_grams) = to_ngrams(
            kwargs['dex_dict']
        )
        kwargs["gen_dict"] = gen_dict
        kwargs["two_grams"] = two_grams
        kwargs["three_grams"] = three_grams
        # Complete config derived from JSON
        return Config(**kwargs)

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
    game_dict: Dict[int, Game]
    gen_dict: Dict[int, List[Game]]

    two_grams: Dict[str, List[int]]
    three_grams: Dict[str, List[int]]

    api_url: str
    ports: Ports

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
