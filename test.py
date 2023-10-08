from pypokedex.exceptions import PyPokedexHTTPError
from argparse import ArgumentParser
from util import set_config
import pypokedex as dex
import pokebase as pb
import asyncio
import uvicorn
import signal
import sys

PORTS = {
    "client": 8080,
    "api": 8000
}

API_PORT = PORTS['api']
CLIENT_PORT = PORTS['client']

parser = ArgumentParser(
                    prog='Pokedoku API',
                    description='Test of Pokedoku API',
                    epilog=f'Using the PokeAPI')

def to_server(port, module, scope):
    config = uvicorn.Config(**{
        "port": port,
        "reload": True,
        "host": "0.0.0.0",
        "app": f"{module}:{scope}_{module}"
    })
    return uvicorn.Server(config)


async def run_server(server):
    await server.serve()


async def run_tasks():

    loop = asyncio.get_event_loop()
    api_server = to_server(API_PORT, 'api', 'pd')
    client_server = to_server(CLIENT_PORT, 'client', 'pd')
    api_task = asyncio.ensure_future(run_server(api_server))
    client_task = asyncio.ensure_future(run_server(client_server))

    async def cancel():
        await api_server.shutdown()
        await client_server.shutdown()
        sys.exit(0)

    tasks = [api_task, client_task]
    # https://github.com/encode/uvicorn/pull/1600
    for job in asyncio.as_completed(tasks):
        try:
            results = await job
        finally:
            await cancel()

if __name__ == "__main__":


    N_DEX = pb.APIResourceList('pokemon-species').count
    print('Updating Pokedex...', flush=True, file=sys.stderr)
    while True:
        N_DEX += 1
        try:
            dex.get(dex=(N_DEX))
        except PyPokedexHTTPError:
            break

    args = parser.parse_args()
    # Configure API
    set_config(**{
        **vars(args), 'ports': PORTS,
        'api_url': 'https://pokeapi.co/api/v2/',
        'ndex': N_DEX,
    })

    # Test the API
    asyncio.run(run_tasks())
