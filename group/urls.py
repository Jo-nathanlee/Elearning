from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('new/<int:course_id>/', views.new,name='new_group'),
    path('<int:course_id>/', views.admin,name='admin'),
    path('edit/<int:group_id>/', views.edit),
    path('delete/<int:group_id>/', views.delete),
    path('forum/<int:group_id>/', views.forum),
    path('post/new/<int:group_id>/', views.new_post), 
    path('post/edit/<int:post_id>/', views.edit_post), 
    path('post/delete/<int:post_id>/', views.delete_post), 
    path('post/<int:post_id>/', views.post), 
    path('comment', views.comment,name='forum_comment'), 
    path('upload_project', views.upload_project,name='upload_project'), 
    path('download_project', views.download_project,name='download_project'), 
]