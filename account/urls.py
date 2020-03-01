from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', views.register,name='register'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('account/', views.account,name='account'),
    path('account/<str:tab>/', views.account_tab),
    path('homework_download/<int:id>/', views.download,name='homework_download'),
]