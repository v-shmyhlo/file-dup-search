import os
import json
from aiohttp import web
import file_duplicate

STORAGE = './search-storage.json'
SEARCH_PATH = '/'


def load_search_results(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)

    return None  # for explicitness


def save_search_results(result, path):
    with open(path, 'w') as f:
        json.dump(result, f)


async def get_search(_request):
    result = load_search_results(STORAGE)

    if result is None:
        return web.HTTPNotFound()

    return web.json_response(result)


async def post_search(_request):
    result = file_duplicate.search(SEARCH_PATH)
    save_search_results(result, STORAGE)

    return web.json_response(result)


def main():
    # port, host, storage, directory for searching are not configurable for this simple example
    # can have race conditions affecting storage with concurrent requests

    app = web.Application()
    app.add_routes([web.get('/search', get_search)])
    app.add_routes([web.post('/search', post_search)])
    web.run_app(app)


if __name__ == '__main__':
    main()
