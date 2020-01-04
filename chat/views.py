from motor import motor_asyncio as ma
import aiohttp_jinja2
from aiohttp import web, WSMsgType
from models import User, users
from chat.models import Message, Contacts
from serializer import JSONEncoder
from aiohttp_session import get_session
from utils import check_pass, set_session
import json


class Hello(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        pass
        # mongo = self.request.app['mongo']
        # document = {'key3': 'value'}
        # result = await mongo.test_collection.insert_one(document)
        # cursor = mongo.test_collection.find()
        # for document in await cursor.to_list(length=100):
        #     value=document
        # session = await get_session(self.request)
        # login = session.get('login')
        # user = await User.query.where(User.login==login).gino.first()
        # return {'name': user.login}


class Login(web.View):
    @aiohttp_jinja2.template('login.html')
    async def get(self):
        pass

    async def post(self):
        data = await self.request.json()
        user = await User.query.where(User.login==data['login']).gino.first()
        if user and await check_pass(data['login'], data['password']):
            session = await get_session(self.request)
            set_session(session, user.login, data['password'])
        return web.Response(status=400, text='Неправильный логин или пароль')


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
                        mongo = Message(self.request.app['mongo']['test_collection'])
                        r = await mongo.save(user='admin', msg=msg.data)
                        await _ws.send_json(r)
            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        self.request.app['websockets'].remove(ws)

        return ws

class ContactList(web.View):
    async def get(self):
        mongo = Contacts(self.request.app['mongo']['test_collection'])
        messages = await mongo.get_messages()
        # document = {'key3': 'value'}
        # result = await mongo.test_collection.insert_one(document)

        # session = await get_session(self.request)
        # login = session.get('login')
        # user = await User.query.where(User.login==login).gino.first()
        return web.Response(status=200, body=JSONEncoder().encode(messages))


class Messages(web.View):
    async def get(self):
        mongo = Message(self.request.app['mongo']['test_collection'])
        messages = await mongo.get_messages()
        # document = {'key3': 'value'}
        # result = await mongo.test_collection.insert_one(document)

        # session = await get_session(self.request)
        # login = session.get('login')
        # user = await User.query.where(User.login==login).gino.first()
        return web.Response(status=200, body=JSONEncoder().encode(messages))

    async def post(self):
        # try:
        data = await self.request.json()
        message = data['message']
        mongo = Message(self.request.app['mongo']['test_collection'])
        # await mongo.save(user = 'admin', msg = data['message'])
        # await mongo.save(user = 'other', msg = data['message'])
        session = await get_session(self.request)
        login = session.get('login')
        msg = await mongo.save(user=login, msg=message)
        for _ws in self.request.app['websockets']:
            await _ws.send_json(msg)
        # document = {'key3': 'value'}
        # result = await mongo.test_collection.insert_one(document)

        # user = await User.query.where(User.login==login).gino.first()
        return web.Response(status=200)
        # except Exception:
        #     return web.Response(status=400)