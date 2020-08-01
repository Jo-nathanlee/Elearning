from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('new', views.new,name='new_group'),
    path('', views.index,name='group_index'),
    path('edit/<int:group_id>/', views.edit),
    path('delete/<int:group_id>/', views.delete),
    path('<int:group_id>/', views.forum),
    path('post/new/<int:group_id>/', views.new_post), 
    path('post/edit/<int:post_id>/', views.edit_post), 
    path('post/delete/<int:post_id>/', views.delete_post), 
    path('post/<int:post_id>/', views.post), 
    path('comment', views.comment,name='forum_comment'), 
    path('upload_project', views.upload_project,name='upload_project'), 
]