
from gino.ext.aiohttp import Gino
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

db = Gino()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), autoincrement=True, primary_key=True)
    login = db.Column(db.Unicode(), default='noname')
    passwd = db.Column(db.Unicode(), default='noname')


# metadata = MetaData()
# users = Table(
#     'users', metadata,
#
#     Column('id', Integer, primary_key=True),
#     Column('login', String),
#     Column('passwd', String),
# )


async def init_db():

	async with db.set_bind('postgres://username:password@localhost:5433/chat_db'):
		await db.gino.create_all()