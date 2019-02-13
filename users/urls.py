from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='users-home'),
    path('user/', views.home, name='users-home'),
    path('user/login/', views.login, name='users-login'),
    path('user/register/', views.register, name='users-register'),
    path('user/logout/', views.logout, name='users-logout'),
    path('user/modules/', views.modules, name='users-modules'),
]