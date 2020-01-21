from models import User
from passlib.hash import pbkdf2_sha256
from time import time
from aiohttp import web

def set_session(session, id, login, password):
    session['id'] = str(id)
    session['login'] = str(login)
    session['password'] = str(password)
    session['last_visit'] = time()
    raise web.HTTPFound('/hello')

def check_path(path):
    result = True
    for r in ['/login', '/static/', '/signin', '/signout', '/registration']:
        if path.startswith(r):
            result = False
    return result

async def create_user(login, password):
    hash = pbkdf2_sha256.encrypt(password)
    await User.create(login=login, passwd=hash)

async def check_pass(login, password):
    user = await User.query.where(User.login == login).gino.first()
    hash = user.passwd
    return pbkdf2_sha256.verify(password, hash)