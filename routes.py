from chat.views import Hello, WebSocket, RoomMessages, Login, Messages

routes = [
    # ('GET', '/',        ChatList,  'main'),
    # ('GET', '/ws',      WebSocket, 'chat'),
    ('*',   '/login',   Login,     'login'),
    # ('*',   '/signin',  SignIn,    'signin'),
    # ('*',   '/signout', SignOut,   'signout'),
    ('GET', '/hello', Hello, 'hello'),
    ('GET', '/room', RoomMessages, 'room'),
    ('*', '/messages', Messages, 'messages'),
    ('GET', '/ws',  WebSocket, 'socket_message')
]