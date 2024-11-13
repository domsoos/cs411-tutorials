# blog/urls.py

from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.index, name='index'),  # Route for the homepage
    path('create/', views.create_post, name='create_post'),  # Route to create a new post
]

