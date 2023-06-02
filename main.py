import os
import hash
import psycopg2
from flask import Flask, render_template

conn = psycopg2.connect(
        host="localhost",
        database="UserInfo",
        user='postgres',
        password='cirilo123'
)

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute('SELECT * FROM accounts')
data = cur.fetchall()
print(data)

app = Flask(__name__)

@app.route("/")
def index():
    cur.execute('SELECT * FROM accounts')
    books = cur.fetchall()
    return render_template('index.html', books=books)