from django.urls import path
from . import views
from .views import (
    ModuleListView,
    ModuleCreateView,
)

# NOTE: using weather's 'views'
urlpatterns = [
    path('', views.home, name='dashboard-home'),
    path('update/', views.update, name='dashboard-update'),
    path('save_update/', views.save_update, name='dashboard-update-save'),
    path('modules/', ModuleListView.as_view(), name='user-modules'),
    path('modules/add/', ModuleCreateView.as_view(), name='add-module')
]