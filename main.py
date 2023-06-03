import os
import hash
import psycopg2
from flask import Flask, render_template, redirect, url_for, request

conn = psycopg2.connect(
        host="localhost",
        database="UserInfo",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
)

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute('SELECT * FROM accounts')
data = cur.fetchall()
hash.pass_encryption(data[0][2])

app = Flask(__name__)

@app.route("/")
def index():
    cur.execute('SELECT * FROM accounts')
    books = cur.fetchall()
    #print(books[0][2])
    return render_template('index.html', books=books)

@app.route("/insert", methods=['POST', 'GET'])
def insert():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    #cur.execute(f'INSERT INTO accounts({username}, {password}, {email}, CURRENT_TIMESTAMP)')
    return f"The username is: {username}, password is {password}, email is: {email}"