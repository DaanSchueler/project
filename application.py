from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from passlib.apps import custom_app_context as pwd_context

import requests
import json
import pprint as pp


from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///recepts.db")

@app.route("/")
@app.route("/index")
def index():

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return ("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return ("must provide password")

        # ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return ("must provide confirmation password")

        # ensure confirmation password and password match
        # if not match return apology
        elif not request.form.get("password") == request.form.get("confirmation"):
            return ("confirmation password and password must match")

        # password omzetten naar hash
        password = request.form.get("password")
        password = pwd_context.hash(password)

        # user in database zetten
        user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashx)",
                          username=request.form.get("username"), hashx=password)

        # als de gebruikersnaam al bestaat
        if not user:
            return ("username already exists")

        # onthou dat de gebruiker ingelogd is
        session["user_id"] = user

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("index"))

@app.route("/search", methods=["GET", "POST"])
def search():

    if request.method == "POST":
        allergy_terms = str()
        diet_terms = str()

        all_allergies = ['gluten-free','peanut-free','seafood-free','sesame-free','soy-free','dairy-free','egg-free','sulfite-free','wheat-free','tree nut-free']
        for checkbox in all_allergies:
            allergy = request.form.get(checkbox)
            if allergy:
                allergy_terms += "&allowedAllergy[]=" + allergy

        all_diets = ["Ketogenic","Lacto vegetarian","Ovo vegetarian","Pescetarian","Vegan","Low FODMAP","Lacto-ovo vegetarian","Paleo"]
        for checkbox in all_diets:
            diet = request.form.get(checkbox)
            if diet:
                diet_terms += "&allowedDiet[]=" + diet

        t = requests.get("http://api.yummly.com/v1/api/recipes?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e&requirePictures=true" + allergy_terms + diet_terms)
        x = json.loads(t.text)
        print(x["criteria"])
        for i in range(len(x["matches"])):
            pp.pprint(x["matches"][i])
            print()

    else:
        return render_template("search.html")