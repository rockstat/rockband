from aiohttp import web
import uvloop
import asyncio

from .log import logger
from .lib.http import say_cors_yes
from . import dome

__all__ = ['add_routes', 'start_server', 'app']
"""
Loop error handler example
https://git.duniter.org/clients/python/sakia/blob/master/src/sakia/main.py
"""


@web.middleware
async def middleware(request, handler):
    """
    Simple CORS middleware to access api from dashboard
    """
    return say_cors_yes(request) if request.method == 'OPTIONS' else await handler(request)

# @web.middleware
async def error_middleware(request, handler):
    """
    Error handling middleware
    """
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return web.json_response({'error': message})



def loop_exc(loop, context):
    message = context.get('message', None)
    exception = context.get('exception', None)
    exc_info = (type(exception), exception,
                exception.__traceback__) if exception else None
    logger.exception('loop ex %s, %s', message, exception, exc_info=exc_info)


loop = uvloop.new_event_loop()
loop.set_exception_handler(loop_exc)
asyncio.set_event_loop(loop)

app = web.Application(logger=logger, debug=False, middlewares=[middleware])


def add_routes(routes):
    app.router.add_routes(routes)


def start_server(listen, name, **kwargs):
    host, port = listen.split(':')
    add_routes(dome.routes)

    web.run_app(app, host=host, port=port, handle_signals=True, print=None)
