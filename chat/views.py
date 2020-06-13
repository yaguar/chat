from motor import motor_asyncio as ma
import aiohttp_jinja2
from aiohttp import web, WSMsgType
from models import User
from chat.models import Message, Contacts, ChatUsers
from serializer import JSONEncoder
from aiohttp_session import get_session
from utils import check_pass, set_session, create_user
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
            set_session(session, user.id, user.login, data['password'])
        return web.Response(status=400, text='Неправильный логин или пароль')


class LoginList(web.View):
    async def get(self):
        search = self.request.rel_url.query['q']
        users = await User.query.where(User.login.contains(search)).gino.all()
        return web.Response(status=200, body=JSONEncoder().encode(users[:10]))


class ChatList(web.View):
    async def get(self):
        mongo = Message(self.request.app['mongo']['users'])
        messages = await mongo.get_messages()
        search = self.request.rel_url.query['q']
        users = await User.query.where(User.login.contains(search)).gino.all()
        return web.Response(status=200, body=JSONEncoder().encode(users[:10]))


class MainInfo(web.View):
    async def get(self):
        request = self.request
        return web.Response(status=200, body=JSONEncoder().encode({'id': request.id, 'login': request.login}))


class Registration(web.View):
    @aiohttp_jinja2.template('registration.html')
    async def get(self):
        pass

    async def post(self):
        data = await self.request.json()
        user = await User.query.where(User.login==data['login']).gino.first()
        if not user and data['password']:
            await create_user(data['login'], data['password'])
            session = await get_session(self.request)
            set_session(session, data['login'], data['password'])
        return web.Response(status=400, text='Данный логин уже существует')


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
        login = self.request.login
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
        chat_id = str(data['chat_id'])
        if chat_id.isdigit():
            if int(self.request.id) <= int(chat_id):
                chat_id = self.request.id + '_' + str(chat_id)
            else:
                chat_id = str(chat_id) + '_' + self.request.id
        mongo = Message(self.request.app['mongo']['messages'][chat_id])
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


class ChatId(web.View):
    async def get(self):
        chat_id = self.request.match_info.get('chat_id', None)
        if chat_id.isdigit():
            if int(self.request.id) <= int(chat_id):
                chat_id = self.request.id + '_' + str(chat_id)
            else:
                chat_id = str(chat_id) + '_' + self.request.id
        mongo = Message(self.request.app['mongo']['messages'][chat_id])
        # await mongo.save(user = 'admin', msg = 'привет')
        # await mongo.save(user = 'other', msg = 'привет')
        # await mongo.save(user='admin', msg='пока')
        # await mongo.save(user='other', msg='пока')
        messages = await mongo.get_messages()
        # document = {'key3': 'value'}
        # result = await mongo.test_collection.insert_one(document)

        # session = await get_session(self.request)
        # login = session.get('login')
        # user = await User.query.where(User.login==login).gino.first()
        return web.Response(status=200, body=JSONEncoder().encode(messages))

    async def post(self):
        # try:
        chat_id = self.request.match_info.get('id', None)
        data = await self.request.json()
        message = data['message']
        mongo_msg = Message(self.request.app['mongo']['messages'][chat_id])
        # mongo_users = ChatUser(self.request.app['mongo']['users'][chat_id])

        # await mongo.save(user = 'admin', msg = data['message'])
        # await mongo.save(user = 'other', msg = data['message'])
        session = await get_session(self.request)
        login = session.get('login')
        msg = await mongo_msg.save(user=login, msg=message)
        for _ws in self.request.app['websockets']:
            await _ws.send_json(msg)
        # document = {'key3': 'value'}
        # result = await mongo.test_collection.insert_one(document)

        # user = await User.query.where(User.login==login).gino.first()
        return web.Response(status=200)
        # except Exception:
        #     return web.Response(status=400)


class ListPerson(web.View):
    async def get(self):
        users = await User.query.gino.all()
        l = list(users)
        # document = {'key3': 'value'}
        # result = await mongo.test_collection.insert_one(document)

        # session = await get_session(self.request)
        # login = session.get('login')
        # user = await User.query.where(User.login==login).gino.first()
        return web.Response(status=200, body=JSONEncoder().encode(users))
    