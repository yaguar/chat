from gino import Gino
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.Unicode(), default='noname')


metadata = MetaData()
users = Table(
    'users', metadata,

    Column('id', Integer, primary_key=True),
    Column('login', String),
    Column('passwd', String),
)