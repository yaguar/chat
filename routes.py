from chat.views import Hello, WebSocket, RoomMessages, Login, Messages, Registration, LoginList, ChatId

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
    ('*', '/messages/{chat_id}', ChatId, 'chat_id'),
    ('GET', '/ws',  WebSocket, 'socket_message')
]