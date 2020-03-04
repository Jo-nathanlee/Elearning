from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('new/', views.new_course,name='new_course'),
    path('', views.course_index,name='courses'),
    path('my_course', views.user_course,name='my_course'),
    path('category/<str:category>/', views.category),
    path('<int:course_id>/', views.course_page),
    path('edit/<int:course_id>/', views.course_edit),
    path('delete/<int:course_id>/', views.course_delete),
    path('new_lesson/<int:course_id>/', views.new_lesson), 
    path('edit_lesson/<int:course_id>/<int:lesson_id>/', views.edit_lesson),
    path('lesson/<int:lesson_id>/<int:lesson_index>/', views.lesson_page),
    path('tab/', views.index_tab,name='tab'),
    path('comment/', views.comment,name='comment'),
    path('reply/', views.reply,name='reply'),
    path('register/', views.register,name='course_register'),
    path('upload_homework/', views.upload_homework,name='upload_homework'),
]