# blog/views.py

from django.shortcuts import render, redirect
from .models import Post  # Import your Post model

def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(title=title, content=content)
        return redirect('index')
    return render(request, 'blog/create_post.html')

