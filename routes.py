from chat.views import Hello, WebSocket, RoomMessages, Login, Messages, Registration, LoginList, ChatId, MainInfo, ChatList

routes = [
    # ('GET', '/',        ChatList,  'main'),
    # ('GET', '/ws',      WebSocket, 'chat'),
    ('*',   '/login',   Login,     'login'),
    ('*',   '/registration',   Registration,     'registration'),
    # ('*',   '/signin',  SignIn,    'signin'),
    # ('*',   '/signout', SignOut,   'signout'),
    ('GET', '/hello', Hello, 'hello'),
    ('GET', '/login_list', LoginList, 'login_list'),
    ('GET', '/chat_list', ChatList, 'chat_list'),
    ('GET', '/main_info', MainInfo, 'main_info'),
    ('GET', '/room', RoomMessages, 'room'),
    ('*', '/messages', Messages, 'messages'),
    ('*', '/messages/{chat_id}', ChatId, 'chat_id'),
    ('GET', '/ws',  WebSocket, 'socket_message')
]