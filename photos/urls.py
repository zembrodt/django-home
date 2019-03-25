from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/images/', views.get_images),
]