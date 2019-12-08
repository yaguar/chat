#! /usr/bin/env python
import asyncio
import aiohttp_jinja2
import aiohttp_debugtoolbar
import jinja2
from aiohttp_session import SimpleCookieStorage, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
# from aiohttp_session.cookie_storage import EncryptedCookieStorage
# from aiohttp_session import session_middleware
# from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp import web

# from routes import routes
# from middlewares import authorize
from motor import motor_asyncio as ma
from settings import *
from routes import routes
import asyncpg
import gino
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from gino.ext.aiohttp import Gino
from models import db
from middleware import authorization

import base64
from cryptography import fernet


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')

async def init_pg(app):
    app['websockets'] = []
    client = ma.AsyncIOMotorClient('mongodb://127.0.0.1:27017')
    mongo = client['chat_db']
    app['mongo'] = mongo
    # engine = await asyncpg.connect(
    #     user='username',
    #     password='password',
    #     database='chat_db',
    #     host='127.0.0.1',
    #     port='5433'
    # )
    # db = Gino()
    #
    # class User(db.Model):
    #     __tablename__ = 'users'
    #
    #     id = db.Column(db.Integer(), primary_key=True)
    #     login = db.Column(db.Unicode(), default='noname')
    # engine = await db.set_bind('postgres://username:password@localhost:5433/chat_db')
    # await db.gino.create_all()
    # app['db'] = engine
    # app['config']['gino'] = {'user': 'username',  'password':'password', 'host':'localhost', 'port':'5433', 'database':'chat_db'}

async def close_pg(app):
    await app['mongo'].close()
    del app['mongo']

# db = Gino()
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
middle = [
    # session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(SECRET_KEY, 'utf-8')).digest())),
    session_middleware(EncryptedCookieStorage(secret_key)),
    authorization,
    db
]

# if DEBUG:
# middle.append(aiohttp_debugtoolbar.middleware)

app = web.Application(middlewares=middle)
app['config'] = {}
app['config']['gino'] = {'user': 'username',  'password':'password', 'host':'localhost', 'port':'5432', 'database':'chat_db'}
db.init_app(app)
# aiohttp_debugtoolbar.setup(app)
# app.on_startup.append(init_pg)
# if DEBUG:
#     aiohttp_debugtoolbar.setup(app)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# route part
for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])
app.router.add_static('/static', 'static', name='static')
# app['static_root_url'] = '/static'
# app.router.add_static('/static', 'static', name='static')
# end route part

# db connect
# app.client = ma.AsyncIOMotorClient(MONGO_HOST)
# app.db = app.client[MONGO_DB_NAME]
# end db connect

# app.on_cleanup.append(on_shutdown)
# app['websockets'] = []

log.debug('start server')
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
web.run_app(app, host='127.0.0.1', port=8000)
log.debug('Stop server end')
