from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from datetime import timedelta
import os, psycopg2, hash


conn = psycopg2.connect(
        host="localhost",
        database="UserInfo",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
)

# Open a cursor to perform database operations
cur = conn.cursor()

app = Flask(__name__)
app.secret_key = "FAKE-KEY"
app.permanent_session_lifetime = timedelta(seconds=60)

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("protected"))
    return render_template(("login.html"), show_error=True)

@app.route("/login", methods=['POST'])
def login():
    # cur.execute('SELECT * FROM accounts')
    # books = cur.fetchall()
    # print(books[0][2])
    # return render_template('index.html', books=books)
    
    if request.method == "POST":
        try:
            user = request.form["username"]
            password = request.form['password']
            session["user"] = user
            cur.execute("SELECT * from accounts WHERE username = %s", [user])
            conn.commit()
            result = cur.fetchall()
            if result == None:
                print("Empty")
            else:
                print(result)
            encrypted_pass = hash.pass_encryption(password)
            #print(result[0][2])
            decrypted_pass = hash.pass_check(result[0][2], password)
            if decrypted_pass:
                return redirect(url_for("protected"))
            else:
                print(decrypted_pass)
                return render_template("login.html", show_error=decrypted_pass)
        except Exception as err:
            return err
        #return redirect(url_for("protected"))
    else:
        if "user" in session:
            return redirect(url_for("protected"))
        return render_template(url_for("login.html"))

@app.route("/insert", methods=['POST', 'GET'])
def insert():
    # email = request.form['email']
    # hpass = hash.pass_encryption(password)
    # cur.execute("INSERT INTO accounts(username, password, email, created_on) VALUES(%s, %s, %s, CURRENT_TIMESTAMP)", [username, hpass, email])
    # cur.execute("SELECT * from accounts WHERE username = %s", [username])
    # result = cur.fetchall()
    # conn.commit()
    # cur.execute("ROLLBACK")
    # conn.commit()
    # return f"The username is: {username}, password is {hpass}, email is: {email}"

    # token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, app.config['SECRET_KEY'])
    return "failed"

@app.route("/protected", methods=["GET"])
def protected():
    if "user" in session:
        user = session["user"]
        return f"{user} private instance"
    else:
        return redirect(url_for("index"))
    
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))