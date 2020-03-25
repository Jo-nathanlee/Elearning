# Import all default settings.
from .settings import *

import dj_database_url
DATABASES = {
    'default':dj_database_url.config()
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'heroku_dc04ad37ecbfba8',
#         'USER': 'bf5322bbb0e06d',
#         'PASSWORD':'c2ac27df',
#         'HOST':'us-cdbr-iron-east-04.cleardb.net',
#         # 'OPTIONS': {'ssl': {'ca':'C:/Users/Jonathan/Desktop/E-Learning/heroku_venv/ca-cert.pem', 'cert':'C:/Users/Jonathan/Desktop/E-Learning/heroku_venv/cert.pem', 'key':'C:/Users/Jonathan/Desktop/E-Learning/heroku_venv/key.pem'}}
#     }
    
# }
STATIC_ROOT = 'staticfiles' 

# Honor the 'X-Forwarded-Proto' header for request.is_secure().
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers.
ALLOWED_HOSTS = ['*']

# Turn off DEBUG mode.
# DEBUG = False