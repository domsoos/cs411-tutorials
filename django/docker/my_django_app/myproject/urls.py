# myproject/urls.py

from django.contrib import admin
from django.urls import path, include  # Import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Include URLs from the 'blog' app
]

