from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='users-home'),
    path('auth/', include('rest_auth.urls')),
    path('auth/register/', include('rest_auth.registration.urls')),
    path('register/', views.register, name='user-register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),
         name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='user-logout'),
    #path('user/modules/', views.modules, name='users-modules'),
    #path('current_user/', views.current_user),
    #path('users/', views.UserList.as_view())
]
