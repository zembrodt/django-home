from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='weather-home'),
    path('update_weather/', views.update_weather_stats, name='weather-update'),
]