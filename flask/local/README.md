# Tutorial 4.1: Local Setup on macOS/Linux and Windows
- Prerequisites
  - Python 3.6+ installed.
  - pip  installed.
  - PostgreSQL installed and running.

## Step 1: Install Python and pip
- macOS/Linux:
  - Verify if Python is pre-installed:
  ```bash
  python3 --version
  ```

  - If not installed, download from the [official website](https://www.python.org/downloads/).
- Windows:
  - Download and install Python from the [official website](https://www.python.org/downloads/windows/). 
  - Make sure you select "Add Python to PATH" during installation.
  - Verify installation:
  ```bash
  python --version
  ```

## Step 2: Install PostgreSQL
- Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/).

## Step 3: Create a Virtual Environment
- macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

- Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

## Step 4: Install Required Python Packages
```bash
pip install Flask psycopg2-binary
```

## Step 5: Set Up PostgreSQL Database
- Create a Database and User
  - Open the PostgreSQL shell:
  ```bash
  psql -U postgres
  ```
  - Create a new database and user:
  ```sql
  CREATE DATABASE mydatabase;
  CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
  GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
  \q
  ```

## Step 6: Create a Simple Flask Application
- Create a file named `app.py`:

