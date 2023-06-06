import os
import hash
import psycopg2

from flask import Flask, render_template, redirect, url_for, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

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

#JWT setup
app.config["JWT_SECRET_KEY"] = "password"  # Change this!
jwt = JWTManager(app)

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
    cur.execute("INSERT INTO accounts(username, password, email, created_on) VALUES(%s, %s, %s, CURRENT_TIMESTAMP)", [username, password, email])
    conn.commit()

    return f"The username is: {username}, password is {password}, email is: {email}"