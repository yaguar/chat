from models import User
from passlib.hash import pbkdf2_sha256
from time import time
from aiohttp import web

def set_session(session, login, password):
    session['login'] = str(login)
    session['password'] = str(password)
    session['last_visit'] = time()
    raise web.HTTPFound('/hello')

def check_path(path):
    result = True
    for r in ['/login', '/static/', '/signin', '/signout']:
        if path.startswith(r):
            result = False
    return result

async def check_pass(login, password):
    user = await User.query.where(User.login == login).gino.first()
    hash = user.passwd
    return pbkdf2_sha256.verify(password, hash)