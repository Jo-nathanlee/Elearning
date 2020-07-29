from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('new', views.new,name='new_group'),
    path('', views.index,name='group_index'),
    path('edit/<int:group_id>/', views.edit),
    path('delete/<int:group_id>/', views.delete),
]