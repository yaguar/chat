from aiohttp import web
import asyncpg
import json
import aiohttp_jinja2
from aiohttp import web, WSMsgType
from models import User, users
# async def hello(request):
#     return web.Response(text="Hello, world")

class Hello(web.View):
    @aiohttp_jinja2.template('hello.html')
    async def get(self):
        # conn = await asyncpg.connect(user='username', password='password',
        #                              database='django_db', host='127.0.0.1', port='5433')

        # await conn.set_type_codec(
        #     'json',
        #     encoder=json.dumps,
        #     decoder=json.loads,
        #     schema = 'pg_catalog'
        # )
        # data = {'username': None}
        # await conn.set_type_codec('json', encoder=json.dumps, decoder=json.loads, schema='pg_catalog')
        # query = db.select([User])
        print(await User.query.gino.all())
        values = await User.query.gino.all()
        # values = await User.select()
        # await db.close()
        dicter = []
        for v in values:
            print(v.login)
        return {'name': [value.login for value in values]}


class RoomMessages(web.View):
    @aiohttp_jinja2.template('room_messages.html')
    async def get(self):
        pass
        # db = self.request.app['db']
        # conn = await asyncpg.connect(user='username', password='password',
        #                              database='django_db', host='127.0.0.1', port='5433')

        # await conn.set_type_codec(
        #     'json',
        #     encoder=json.dumps,
        #     decoder=json.loads,
        #     schema = 'pg_catalog'
        # )
        # data = {'username': None}
        # await conn.set_type_codec('json', encoder=json.dumps, decoder=json.loads, schema='pg_catalog')
        # values = await db.fetch('''SELECT username FROM auth_user''')
        # await db.close()

        # return {'name': [value['username'] for value in values]}


class WebSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        # session = await get_session(self.request)
        # user = User(self.request.db, {'id': session.get('user')})
        # login = await user.get_login()

        # for _ws in self.request.app['websockets']:
        #     _ws.send_str('%s joined' % login)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    for _ws in self.request.app['websockets']:
                        await _ws.send_str(msg.data)
            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        self.request.app['websockets'].remove(ws)
        print('websocket connection closed')

        return ws
