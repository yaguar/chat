import logging


log = logging.getLogger('app')
log.setLevel(logging.DEBUG)

f = logging.Formatter('[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt = '%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)
log.addHandler(ch)


DEBUG = True

SITE_HOST = '127.0.0.1'
SITE_PORT = '8000'
SECRET_KEY = 'fhfghjrterg'

MESSAGE_COLLECTION = 'messages'
USER_COLLECTION = 'users'