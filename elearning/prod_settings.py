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

AWS_ACCESS_KEY_ID = 'AKIAYVUJYZ5X53HOSM55'
AWS_SECRET_ACCESS_KEY = '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'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'elearning-upload-heroku'
AWS_S3_REGION_NAME = 'ap-southeast-1'

SHARED_SESSION_SITES = [ 'elearning-chat.herokuapp.com']