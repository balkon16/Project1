import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

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
    username = request.form.get("username") #obowiązkowy
    pwd = request.form.get("pwd") #obowiązkowy
    pwd_rep = request.form.get("pwd_rep") #obowiązkowy

    if username == "" or pwd == "" or pwd_rep == "":
        message = "Please provide a username and a password"
        return render_template("error.html", message=message)

    if db.execute("SELECT * FROM users WHERE login = :username",
            {"username": username}).rowcount > 0:
            message="User already registered."
            return render_template("error.html", message=message)
    if pwd != pwd_rep:
        message="Passwords must match."
        return render_template("error.html", message=message)

    db.execute("INSERT INTO users (login, pwd, email, first_name, last_name)\
                    VALUES (:username, :pwd, :email, :first_name, :last_name)",
                    {"username": username, "pwd": pwd, "email": email, \
                    "first_name": first_name, "last_name": last_name})
    db.commit()
    message = "New user has been added."
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

@app.route("/api/<string:isbn>")
def goodreads(isbn):
    #TODO1: obsługa istniejących ISBN działa; nie wiem jak obsługiwać
    #niepoprawne ISBN
    #TODO2: wyświetlać wybrane pola w ładnym formacie

    # https://www.goodreads.com/api/index#book.show_by_isbn <-- chodzi o tą metodę GET
    #poniższa strona zawiera potrzebne mi dane; muszę zczytać XML w Pythonie:
    #https://www.goodreads.com/book/isbn/0441172717?key=wfxe1FhSbZOGjXSrWulWVQ

    ###example from project's website
    # res = requests.get("https://www.goodreads.com/book/review_counts.json",
    # params={"key": "wfxe1FhSbZOGjXSrWulWVQ", "isbns": isbn})
    ###

    res1 = requests.get("https://www.goodreads.com/book/isbn_to_id/{}?key={}".format(isbn, "wfxe1FhSbZOGjXSrWulWVQ"))
    book_id = res1.json()

    res2 = requests.get("https://www.goodreads.com/book/isbn/{}?key={}".format(isbn, "wfxe1FhSbZOGjXSrWulWVQ"))
    #full_book = res2.json()

    res3 = requests.get("https://www.goodreads.com/book/isbn",
                        params={"key": "wfxe1FhSbZOGjXSrWulWVQ", "isbn": isbn, "format": "json"})



    return render_template("success.html", message=res3.json())
