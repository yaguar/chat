from chat.views import Hello, WebSocket, RoomMessages, Login, Messages, Registration, LoginList

routes = [
    # ('GET', '/',        ChatList,  'main'),
    # ('GET', '/ws',      WebSocket, 'chat'),
    ('*',   '/login',   Login,     'login'),
    ('*',   '/registration',   Registration,     'registration'),
    # ('*',   '/signin',  SignIn,    'signin'),
    # ('*',   '/signout', SignOut,   'signout'),
    ('GET', '/hello', Hello, 'hello'),
    ('GET', '/login_list', LoginList, 'login_list'),
    ('GET', '/room', RoomMessages, 'room'),
    ('*', '/messages', Messages, 'messages'),
    ('GET', '/ws',  WebSocket, 'socket_message')
]