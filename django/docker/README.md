# Tutorial 4.2: Full-Stack Django Application with MySQL using Docker


- Prereqs: 
  - Django installation

## Step 1: Create Django Project
- Create a project directory:
  - For both Windows and macOS/Linux:
  ```bash
  mkdir my_django_app && cd my_django_app=
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
    image: mysql:5.7
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
    # Your apps
    'blog',
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
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': '3306',
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

- Add `'blog'` to `INSTALLED_APPS` in `myproject/settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'blog',
]
```

## Step 6: Defining Models




## Step 7: 3 Building and Running the Docker Containers


## Step 8: Building the Frontend

# Step 9: 
