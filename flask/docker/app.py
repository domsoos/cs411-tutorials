import os
from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'mydatabase'),
            user=os.environ.get('DB_USER', 'myuser'),
            password=os.environ.get('DB_PASS', 'mypassword')
        )
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return f"Database version: {db_version}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False,  threaded=False)

