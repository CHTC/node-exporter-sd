import asyncio
from aiohttp import ClientSession, web
import os

async def fetch_hostnames(session):
    async with session.get(os.environ.get("HOSTNAMES_URL", "http://localhost/cblr/svc/op/list/what/systems")) as response:
        response.raise_for_status()
        text = await response.text()
        return text.splitlines()

async def get_targets():
    async with ClientSession() as session:
        try:
            hostnames = await fetch_hostnames(session)
            targets = [{'targets': [f'{host}:9100' for host in hostnames]}]
            return targets
        except Exception as e:
            print(f'Error getting targets: {e}')
            return []

async def handle_discovery(_):
    targets = await get_targets()
    return web.json_response(targets)

async def init_app():
    app = web.Application()
    app.add_routes([web.get('/node_exporter_sd', handle_discovery)])    
    return app

def main():
    app = asyncio.run(init_app())
    web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
