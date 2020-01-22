from datetime import datetime


class Message():

    def __init__(self, collection):
        self.collection = collection

    async def save(self, user, msg):
        result = await self.collection.insert_one({'user': user, 'msg': msg, 'time': datetime.now()})
        return {'user': user, 'msg': msg, 'time': str(datetime.now())}

    async def get_messages(self):
        messages = self.collection.find().sort([('time', 1)])
        return await messages.to_list(length=None)


class ChatUser():

    def __init__(self, collection, **kwargs):
        self.collection = collection

    async def save(self, user, **kw):
        result = await self.collection.insert_one({'user': user, 'time': datetime.now()})
        return {'user': user, 'time': str(datetime.now())}

    async def get_users(self):
        users = self.collection.find().sort([('time', 1)])
        return await users.to_list(length=None)


class Contacts():
# Удалить
    def __init__(self, collection, **kwargs):
        self.collection = collection

    async def save(self, user, msg, **kw):
        result = await self.collection.insert_one({'user': user, 'msg': msg, 'time': datetime.now()})
        return {'user': user, 'msg': msg, 'time': str(datetime.now())}

    async def get_messages(self):
        messages = self.collection.find().sort([('time', 1)])
        return await messages.to_list(length=None)