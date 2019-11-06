#! /usr/bin/env python
import asyncio
import aiohttp_jinja2
import aiohttp_debugtoolbar
import jinja2
from aiohttp_session import session_middleware
# from aiohttp_session.cookie_storage import EncryptedCookieStorage
# from aiohttp_session import session_middleware
# from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp import web

# from routes import routes
# from middlewares import authorize
# from motor import motor_asyncio as ma
from settings import *
from routes import routes
import asyncpg
import gino
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from models import User

import hashlib


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')

async def init_pg(app):
    app['websockets'] = []
    # engine = await asyncpg.connect(
    #     user='username',
    #     password='password',
    #     database='chat_db',
    #     host='127.0.0.1',
    #     port='5433'
    # )
    metadata = MetaData()
    users = Table(
        'users', metadata,

        Column('id', Integer, primary_key=True),
        Column('login', String),
        Column('passwd', String),
    )
    engine = await gino.create_engine('postgres://username:password@localhost:5433/chat_db')
    await GinoSchemaVisitor(metadata).create_all(engine)
    app['db'] = engine

async def close_pg(app):
    await app['db'].close()
    del app['db']

middle = [
    # session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(SECRET_KEY, 'utf-8')).digest())),
    # authorize,
]

# if DEBUG:
# middle.append(aiohttp_debugtoolbar.middleware)

app = web.Application(middlewares=middle)
# aiohttp_debugtoolbar.setup(app)
# app.on_startup.append(init_pg)
# if DEBUG:
#     aiohttp_debugtoolbar.setup(app)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# route part
for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])
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
