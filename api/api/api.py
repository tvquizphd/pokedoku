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
Post selection, make guess
'''

@pd_api.post("/api/selection", status_code=_201)
async def create_selection(
        e: HasPokemon, config=Depends(to_config)
    ):
    async def post_pokemon():
        return None
#        endpoint = 'pokemon'
#        data = json.loads(e.json())
#        await to_service(config).post_api(endpoint, data)
    # Submit request in parallel
    pool.submit(asyncio.run, post_pokemon())

@pd_api.get("/api/matches")
def get_matches(
        config=Depends(to_config), guess: str = ''
    ):
    return to_service(config).get_matches(guess)
