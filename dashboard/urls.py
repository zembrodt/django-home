from django.urls import path
from . import views
from .views import (
    ModulesListView,
)

# NOTE: using weather's 'views'
urlpatterns = [
    path('', views.home, name='dashboard-home'),
    path('update/', views.update, name='dashboard-update'),
    path('save_update/', views.save_update, name='dashboard-update-save'),
    path('modules/', ModulesListView.as_view(), name='user-modules'),
]