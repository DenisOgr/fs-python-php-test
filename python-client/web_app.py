from aiohttp import web
#from worker import Worker
import json


async def index(request):
    commands = {
        'message': 'Hello I`m mister1 Missix and I can do :',
    }

    return web.Response(text=json.dumps(commands))

# async def get_result(request):
#     worker = Worker()
#     result = worker.process()
#
#     return web.Response(text=result)

web_app = web.Application()
web_app.router.add_get('/', index)
#web_app.router.add_get('/get_result', get_result)
