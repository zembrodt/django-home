from django.urls import path
from . import views

urlpatterns = [
    path('update_forecast/', views.update_forecast_stats, name='forecast-update'),
    path('current/', views.update_forecast_stats),
]