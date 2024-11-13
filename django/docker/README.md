# Tutorial 4.2: Full-Stack Django Application with MySQL using Docker


- Prereqs: 
  - Django installation

## Step 1: Create Django Project
- Create a project directory:
  - For both Windows and macOS/Linux:
  ```bash
  mkdir my_django_app && cd my_django_app
  ```

- Create a `requirements.txt` file:
  ```text
  Django
  mysqlclient
  ``` 

- Create the Django Project using Docker:
We'll use a temporary Docker container to create the Django Project, ensuring the environment in consistent. 

  - Windows
  ```cmd
  docker run --rm -v %cd%:/app -w /app python:3.9-slim bash -c "pip install Django && django-admin startproject myproject ."
  ```
  - macOS/Linux:
  ```bash
  docker run --rm -v $(pwd):/app -w /app python:3.9-slim bash -c "pip install Django && django-admin startproject myproject ."
  ```

## Step 2: Writing the Dockerfile
- Create a `dockerfile` in the project root
```dockerfile
# Use the official Python image
FROM python:3.9-slim

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
# we need gcc, make, mysqlclinet, and pkg-config to compile application
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install more dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Step 3: Create a docker-compose file
- Create a `docker-compose.yml` file in the project root:
```yaml
version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/usr/src/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_HOST=db
      - DATABASE_NAME=django_app
      - DATABASE_USER=django_user
      - DATABASE_PASSWORD=password

  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_DATABASE: django_app
      MYSQL_USER: django_user
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: password
    ports:
      - "3306:3306"
```


## Step 4: Adjust Django Settings:
- Update the `myproject/settings.py` to use environment variables

```python
# myproject/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'  # Replace with your actual secret key

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',  # Use the AppConfig class
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME', 'django_app'),
        'USER': os.environ.get('DATABASE_USER', 'django_user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'password'),
        'HOST': os.environ.get('DATABASE_HOST', 'db'),
        'PORT': '3306',
        'OPTIONS': {
            'auth_plugin': 'mysql_native_password',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # Add other validators as needed
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```


- Create a `.env` file in the project root:
```text
DATABASE_HOST=db
DATABASE_NAME=django_app
DATABASE_USER=django_user
DATABASE_PASSWORD=password
```

- Update the `docker-compose.yml` to load the environment variables:
```yml
web:
  # ...
  env_file:
    - ./.env
```

## Step 5: Create the Django App
- Run the following command to start a new app:
```bash
docker-compose run web python manage.py startapp blog
```

- Verify the app has been created:
  - You should see a new directory named `blog` in your project root.

## Step 6: Defining Models
- Edit `blog/models.py`:
```python
# blog/models.py

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
```

- Create and Apply Migrations:
```bash
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```


## Step 7: 3 Building and Running the Docker Containers
- Building the Docker Images 
```bash
docker-compose build
```

- Running the Containers
  - Start the Containers
  ```bash
  docker-compose up -d
  ```
  - The `-d` flag runs the containers in the detached mode

- Applying the Migrations
  - Run Migrations inside the web container:
  ```bash
  docker-compose exec web python manage.py migrate
  ```
  - Create a Superuser (optional):
  ```bash
  docker-compose exec web python manage.py createsuperuser
  ```


## Step 8: Building the Frontend
- Creating Views and Templates:
  - Edit `blog/views.py`:
  ```python  
  # blog/views.py
  
  from django.shortcuts import render, redirect
  from .models import Post
  
  def index(request):
      posts = Post.objects.all()
      return render(request, 'blog/index.html', {'posts': posts})
  
  def create_post(request):
      if request.method == 'POST':
          title = request.POST['title']
          content = request.POST['content']
          Post.objects.create(title=title, content=content)
          return redirect('index')
      return render(request, 'blog/create_post.html')
  ```

  - Create `blog/urls.py`:
  ```python
  # blog/urls.py
  
  from django.urls import path
  from . import views
  
  urlpatterns = [
      path('', views.index, name='index'),
      path('create/', views.create_post, name='create_post'),
  ]
  ```

  - Include `blog.urls` in `myproject/urls.py`
  ```python
  # myproject/urls.py
  
  from django.contrib import admin
  from django.urls import path, include
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('', include('blog.urls')),
  ]
  ```

  - Create Templates Director and Files:
  ```bash
  mkdir -p blog/templates/blog
  ```

  - Create `index.html` in `blog/templates/blog/`:
  ```html
  <!DOCTYPE html>
  <html>
  <head>
      <title>Posts</title>
  </head>
  <body>
      <h1>Posts</h1>
      <a href="{% url 'create_post' %}">Create New Post</a>
      <ul>
          {% for post in posts %}
          <li>{{ post.title }}: {{ post.content }}</li>
          {% endfor %}
      </ul>
  </body>
  </html>
  ```

  - Create `create_post.html` in `blog/templates/blog/`:
  ```html
  <!DOCTYPE html>
  <html>
  <head>
      <title>Create Post</title>
  </head>
  <body>
      <h1>Create a New Post</h1>
      <form method="post">
          {% csrf_token %}
          <label for="title">Title:</label><br>
          <input type="text" id="title" name="title"><br><br>
          <label for="content">Content:</label><br>
          <textarea id="content" name="content"></textarea><br><br>
          <input type="submit" value="Submit">
      </form>
  </body>
  </html>
  ```


## Step 9: Run Migrations
- Make migrtations:
  ```bash
  docker-compose exec web python manage.py makemigrations
  ```

- Apply Migrations:
  ```bash
  docker-compose exec web python manage.py migrate
  ```

  If everything is configured correctly, these commands should execute without errors.

- Expected Structure:
```markdown
my_django_app/
├── blog/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── templates/
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── requirements.txt
```


  - Connecting Frontend to Backend
  Open your browser and navigate to `http://localhost:8000/`.





