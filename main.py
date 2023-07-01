from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from datetime import timedelta
import os, psycopg2, hash, requests


conn = psycopg2.connect(
        host="localhost",
        database="UserInfo",
        user=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"]
)

# Open a cursor to perform database operations
cur = conn.cursor()

app = Flask(__name__, static_folder="staticFiles")
app.secret_key = "FAKE-KEY"
app.permanent_session_lifetime = timedelta(minutes=10)

@app.route("/")
def index():
    if "user" in session:
        print(session)
        return redirect(url_for("protected"))
    return render_template(("login.html"), show_error=True)

@app.route("/login", methods=['POST'])
def login():
    # cur.execute('SELECT * FROM accounts')
    # books = cur.fetchall()
    # print(books[0][2])
    # return render_template('index.html', books=books)
    
    if request.method == "POST":
        #Gets user and pass from login.html form
        user = request.form["username"]
        password = request.form['password']

        #Checks if user exists in db
        cur.execute("SELECT * from accounts WHERE username = %s", [user])
        conn.commit()
        result = cur.fetchone()
        #Checks if password matches 
        if result == None:
            return "user not found"
        else:
            decrypted_pass = hash.pass_check(result[2], password)

        #Checks if result is empty if not add user info to session
        if result != "" and decrypted_pass == True:
            session["user"] = user
            return redirect(url_for("protected"))
        elif result == None:
            # add in user not found create account
            print("Empty")
        else:
            return render_template("login.html", show_error=decrypted_pass)
        
    else:
        if "user" in session:
            return redirect(url_for("protected"))
        return render_template(url_for("login.html"))

@app.route("/insert", methods=['POST', 'GET'])
def insert():
    try:
        user = request.form["username"]
        password = request.form['password']
        email = request.form['email']
        hpass = hash.pass_encryption(password)
        cur.execute("INSERT INTO accounts(username, password, email, created_on) VALUES(%s, %s, %s, CURRENT_TIMESTAMP)", [user, hpass, email])
        conn.commit()
    except:
        return "Failed"
    finally:
        return render_template("login.html")

@app.route("/protected", methods=["GET"])
def protected():
    if "user" in session:
        user = session["user"]
        response = requests.get("https://jsonplaceholder.typicode.com/posts")
        data = response.json()
        return render_template("data.html", data=data)
    else:
        return redirect(url_for("index"))
    
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))