from django.urls import path
from . import views
from .views import ModuleListView

# NOTE: using weather's 'views'
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update/', views.update, name='dashboard-update'),
    path('dashboard/save_update/', views.save_update, name='dashboard-update-save'),
    path('modules/', ModuleListView.as_view(), name='user-modules'),
    path('modules/add/', views.module_create, name='add-module'),
    path('modules/add/form/', views.get_extended_form, name='add-module-form'),
    path('modules/<int:pk>/update/', views.module_update, name='update-module'),
    path('modules/<int:pk>/delete/', views.module_delete, name='delete-module')
]