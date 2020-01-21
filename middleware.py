from aiohttp import web
from aiohttp.web import middleware
from aiohttp_session import get_session
from utils import check_pass, check_path


@middleware
async def authorization(request, handler):

    session = await get_session(request)
    id = session.get('id')
    login = session.get('login')
    password = session.get('password')
    if not login and check_path(request.path) or login and not await check_pass(login, password):

        # url = request.app.router['login'].canonical
        raise web.HTTPFound('/login')
    request.login = login
    request.id = id
    return await handler(request)


# @middleware
# async def permission(request, handler):
#
#     if request.path == 'messages' and request.method == 'POST':
#
#         raise web.HTTPFound('/login')
#     request.login = login
#     request.id = id
#     return await handler(request)