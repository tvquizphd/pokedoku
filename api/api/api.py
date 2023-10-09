from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY as _422
from starlette.status import HTTP_201_CREATED as _201
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor
from fastapi.responses import JSONResponse
from starlette.requests import Request
from fastapi import Depends, FastAPI
from util.models import HasPokemon
from api.service import to_service
from util import to_config
import asyncio
import json

# Construct API
pd_api = FastAPI()
pd_api.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

pool = ThreadPoolExecutor(max_workers=1)

# Handle common FastAPI exceptions
@pd_api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    content = {'status_code': 10422, 'data': None}
    print(f'{exc}'.replace('\n', ' ').replace('   ', ' '))
    return JSONResponse(content=content, status_code=_422)

'''
TODO: Documentation for Development
'''

@pd_api.get("/api")
def open_root_api(config=Depends(to_config)):
    return { **vars(config) }

'''
Constants
'''

@pd_api.get("/api/regions")
def get_forms(
        config=Depends(to_config)
    ):
    return to_service(config).all_regions

'''
Pokemon forms and search
'''

@pd_api.get("/api/forms")
def get_forms(
        config=Depends(to_config), dexn: str = ''
    ):
    return to_service(config).get_forms(dexn)

@pd_api.get("/api/matches")
def get_matches(
        config=Depends(to_config), guess: str = ''
    ):
    return to_service(config).get_matches(guess)

'''
Validate guess
'''

@pd_api.get("/api/test")
def run_test(
        config=Depends(to_config),
        identifier: str = '',
        conditions: str = ''
    ):
    # Comparison against conditions
    str_cmp = lambda x, y: x.lower() == y.lower()
    fns = [
        (s, lambda x,arr: any([str_cmp(x,y) for y in arr]))
        for s in conditions.split(',')
    ]
    return to_service(config).run_test(identifier, fns)
