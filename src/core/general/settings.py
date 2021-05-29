import os

PROJECT_ROOT_PATH = os.getenv('PROJ_ROOT', '/addr')
# Database related settings
DB_SYSTEM_USER = 'system'
DB_USER = 'addruser'
DB_HOST = 'localhost'
DB_PORT = 5432
CURRENT_DB = os.getenv('PGDATABASE', 'addrmain')

# Log related settings

# logging level
LOGGING_LEVEL = 10
LOGGING_SCREEN = True
LOG_PATH = PROJECT_ROOT_PATH + '/ops/logs/apps/'

# System related settings
ENVIRONMENT = 'dev'
if os.getenv('ENVIRONMENT', 'dev') == 'prod':
    ENVIRONMENT = 'prod'

if ENVIRONMENT == 'prod':
    LOGGING_LEVEL = 40

SYSTEM_USER = 'system'


# Django Path
DJANGO_PATH = PROJECT_ROOT_PATH + '/src/django/addr'


# EMail setting

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = os.getenv('EMAILPASSWORD', '')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = ''
ADMIN = [('desh', 'maildesh@gmail.com')]
EMAIL_SUBJECT_PREFIX = ''

EMAIL_TO = ['maildesh@gmail.com']


DOCUMENT_PATH = PROJECT_ROOT_PATH + '/external/documents/'
