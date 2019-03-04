from django.urls import path
from . import views

urlpatterns = [
    path('update_weather/', views.update_weather_stats, name='weather-update'),
]