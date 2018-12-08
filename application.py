import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

#Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("home_page.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/reset")
def reset():
    return render_template("reset.html", message="")

@app.route("/logout")
def logout():
    #trzeba dodać coś co wyłącza sesje użytkownika;
    #na razie mam tylko layout strony
    return render_template("logout.html")

@app.route("/register_next", methods=["POST"])
def register_next():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    username = request.form.get("username")
    pwd = request.form.get("pwd")
    pwd_rep = request.form.get("pwd_rep")
    message = "test message"
    return render_template("success.html", message=message)

@app.route("/login_next", methods=["POST"])
def login_next():
    login = request.form.get("login")
    pwd = request.form.get("inputPassword")
    if db.execute("SELECT * FROM users WHERE login = :login AND pwd = :pwd",
        {"login": login, "pwd": pwd}).rowcount == 0:
        message = "Wrong username or password."
        return render_template("error.html", message=message)
    message="Login completed!"
    return render_template("success.html", message=message)

@app.route("/check_reset", methods=["POST"])
def check_reset():
    email = request.form.get("email_reset_pwd")
    if email == "":
        message="We need your email address."
        return render_template("error.html", message=message)
    if db.execute("SELECT * FROM users WHERE email = :email",
        {"email": email}).rowcount == 0:
        message="You are not registered or you haven't used your email address."
        return render_template("error.html", message=message)
    message="Please check you inbox."
    return render_template("success.html", message=message)
