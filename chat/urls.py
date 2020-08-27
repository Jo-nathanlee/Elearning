# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<group_id>[^/]+)/$', views.room, name='room'),
    
]