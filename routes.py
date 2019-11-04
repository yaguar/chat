# from chat.views import ChatList, WebSocket
# from auth.views import Login, SignIn, SignOut
from chat.views import Hello, WebSocket, RoomMessages


routes = [
    # ('GET', '/',        ChatList,  'main'),
    # ('GET', '/ws',      WebSocket, 'chat'),
    # ('*',   '/login',   Login,     'login'),
    # ('*',   '/signin',  SignIn,    'signin'),
    # ('*',   '/signout', SignOut,   'signout'),
    ('GET', '/hello', Hello, 'hello'),
    ('GET', '/room', RoomMessages, 'room'),
    ('GET', '/ws',  WebSocket, 'socket_message')
]