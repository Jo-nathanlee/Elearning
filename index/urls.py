from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('teacher', views.teacher, name='teacher'),
]