# Tutorial 4.1: Building a Full-Stack Django Application with MySQL Locally (Windows and macOS/Linux)

In this tutorial, we'll build a simple web application that allows users to create and view posts. We'll use Django for the backend, MySQL for the database, and Django's templating system for the frontend. Instructions will be provided for both Windows and macOS/Linux systems.


- Prerequisites
  - Download MySQL Installer: Visit the MySQL Community Downloads page.
  - Run the Installer:

Choose "Custom" installation to select only the necessary components.
Install MySQL Server and MySQL Workbench (optional).
Configure MySQL Server:
Set the root password (remember this for later).
Use the default port 3306.
Add MySQL to PATH (if not done automatically):
Go to System Properties > Environment Variables.
Edit the Path variable and add the path to your MySQL bin directory (e.g., C:\Program Files\MySQL\MySQL Server 8.0\bin).
Verify the Installation:
Open Command Prompt and run:

```bash
mysql --version
```

macOS/Linux
macOS:

Using Homebrew:

bash
Copy code
brew update
brew install mysql
Start MySQL Server:

bash
Copy code
brew services start mysql
Linux (Ubuntu/Debian):

Install MySQL Server:

bash
Copy code
sudo apt-get update
sudo apt-get install mysql-server
Secure Installation:

bash
Copy code
sudo mysql_secure_installation
Set the root password.
Follow the prompts to secure your installation.
Common Steps for Both Platforms
Access the MySQL Shell:

bash
Copy code
mysql -u root -p
Enter the root password you set during installation.
Create a New Database and User:

sql
Copy code
CREATE DATABASE django_app CHARACTER SET UTF8;
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON django_app.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
<a name="virtual-environment"></a>

Creating a Virtual Environment
It's a good practice to use a virtual environment to manage your project's dependencies.

Windows
Open Command Prompt:

cmd
Copy code
cd C:\path\to\your\project
python -m venv venv
venv\Scripts\activate
The prompt should change to indicate that you're in a virtual environment.
Upgrade pip (optional but recommended):

cmd
Copy code
python -m pip install --upgrade pip
macOS/Linux
Open Terminal:

bash
Copy code
cd /path/to/your/project
python3 -m venv venv
source venv/bin/activate
Upgrade pip:

bash
Copy code
pip install --upgrade pip
<a name="install-django"></a>

Installing Django and MySQL Client
Windows
Install Django:

cmd
Copy code
pip install django
Install mysqlclient:

You may need to install Microsoft Visual C++ Build Tools if you encounter errors.

Download from here.
Then install mysqlclient:

cmd
Copy code
pip install mysqlclient
macOS/Linux
Install Dependencies (if necessary):

macOS:

bash
Copy code
brew install mysql
export PATH="/usr/local/mysql/bin:$PATH"
Linux:

bash
Copy code
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
Install Django and mysqlclient:

bash
Copy code
pip install django
pip install mysqlclient
<a name="create-project"></a>

4. Creating the Django Project Locally
<a name="start-project"></a>

Starting a New Project
Both Windows and macOS/Linux
Create a Django Project:

bash
Copy code
django-admin startproject myproject
cd myproject
<a name="configure-database"></a>

Configuring MySQL Database Settings
Edit myproject/settings.py:

python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_app',
        'USER': 'django_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
<a name="create-app"></a>

Creating a Django App
Create an App Called blog:

bash
Copy code
python manage.py startapp blog
Add blog to INSTALLED_APPS in myproject/settings.py:

python
Copy code
INSTALLED_APPS = [
    # ...
    'blog',
]
<a name="define-models"></a>

Defining Models
Edit blog/models.py:

python
Copy code
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
<a name="run-migrations"></a>

Running Migrations
Make Migrations:

bash
Copy code
python manage.py makemigrations
Apply Migrations:

bash
Copy code
python manage.py migrate
<a name="frontend"></a>

5. Building the Frontend
<a name="views-templates"></a>

Creating Views and Templates
Edit blog/views.py:

python
Copy code
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
Create blog/urls.py:

python
Copy code
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_post, name='create_post'),
]
Include blog.urls in myproject/urls.py:

python
Copy code
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
Create Templates:

Create directory:

Windows:

cmd
Copy code
mkdir blog\templates\blog
macOS/Linux:

bash
Copy code
mkdir -p blog/templates/blog
Create index.html in blog/templates/blog/:

html
Copy code
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
Create create_post.html in blog/templates/blog/:

html
Copy code
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
<a name="connect-frontend-backend"></a>

Connecting Frontend to Backend
Ensure that your views are correctly linked to the templates and that data flows between the frontend and backend.

<a name="run-local"></a>

6. Running the Application Locally
Start the Development Server:

bash
Copy code
python manage.py runserver
Note: If you're on Windows and using Command Prompt, use python instead of python3 if python3 is not recognized.
Access the Application:

Open a web browser and navigate to http://localhost:8000/.
<a name="conclusion"></a>

7. Conclusion
You've successfully built a full-stack Django application connected to a MySQL database on your local machine. You've also learned how to set up the development environment on both Windows and macOS/Linux systems. This setup provides a solid foundation for further development and scaling.
