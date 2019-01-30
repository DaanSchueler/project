from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from passlib.apps import custom_app_context as pwd_context

import requests
import json
import pprint as pp
import ctypes
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

    results = db.execute("SELECT recipe_id, recipe_name, recipe_image, count(recipe_name) AS total FROM likes GROUP BY recipe_name ORDER BY total DESC ")
    check = session.get("user_id")
    likes_set = {}

    if check:
        likes = db.execute("SELECT recipe_id FROM LIKES WHERE id = :id", id= session["user_id"])

        likes_set= {like["recipe_id"] for like in likes}

    return render_template("index.html", results = results, likes = likes_set)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # if not username submitted, show flash message
        if not request.form.get("username"):
            flash("Must provide username")
            return render_template("login.html")

        # if not password submitted, show flash message
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("login.html")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
           flash("Must provide username")
           return render_template("register.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("register.html")

        # ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            flash("Must provide confirmation password")
            return render_template("register.html")

        # ensure confirmation password and password match
        elif not request.form.get("password") == request.form.get("confirmation"):
            flash("Confirmation password and password must match")
            return render_template("register.html")

        # convert password to hash
        password = request.form.get("password")
        password = pwd_context.hash(password)

        # insert user into database
        user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashx)",
                          username=request.form.get("username"), hashx=password)

        # if the username exists then show flash message
        if not user:
            flash("User already exists")
            return render_template("register.html")

        # remember that the user has logged in
        session["user_id"] = user
        session["username"] = request.form.get("username")

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
    """Serach by selected filter and api call """

    if request.method == "POST":
        allergy_terms = str()
        diet_terms = str()
        course_terms = str()
        all_checked = str()

        all_allergies = ['Gluten-free','Peanut-free','Seafood-free','Sesame-free','Soy-free','Dairy-free','Egg-free','Sulfite-free','Wheat-free','Tree nut-free']
        for checkbox in all_allergies:
            allergy = request.form.get(checkbox)
            if allergy:
                all_checked += checkbox + ", "
                allergy_terms += "&allowedAllergy[]=" + allergy

        all_diets = ["Ketogenic","Lacto vegetarian","Ovo vegetarian","Pescetarian","Vegan","Low FODMAP","Lacto-ovo vegetarian","Paleo"]
        for checkbox in all_diets:
            diet = request.form.get(checkbox)
            if diet:
                all_checked += checkbox + ", "
                diet_terms += "&allowedDiet[]=" + diet

        all_courses = ["Main Dishes","Desserts","Side Dishes","Appetizers","Salads","Breakfast and Brunch","Breads","Soups","Beverages","Condiments and Sauces","Cocktails","Snacks","Lunch"]
        for checkbox in all_courses:
            course = request.form.get(checkbox)
            if course:
                all_checked += checkbox + ", "
                course_terms += "&allowedCourse[]=" + course

        all_checked = all_checked[0: -2]

        t = requests.get("http://api.yummly.com/v1/api/recipes?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e&requirePictures=true" + allergy_terms + diet_terms + course_terms)
        x = json.loads(t.text)

        recepten = x["matches"]

        # Render the results of the search on a new page named results 
        return render_template("results.html", recepten=recepten, all_checked=all_checked)

    # if no filters selected render searc page again
    else:
        return render_template("search.html")


@app.route("/moreinfo", methods=["GET", "POST"])
def moreinfo():
    """Renders spscific recipie"""

    if request.method == "POST":
        user = request.form.get("user")
        
        results = db.execute("SELECT * FROM likes WHERE username = :username GROUP BY recipe_name",
                        username = user )
        likes_set = liked(session)

        return render_template("profile.html", results = results, likes = likes_set)

    recipe_id = request.args.get('id')
    recipe_id = recipe_id[1:]

    q = requests.get("http://api.yummly.com/v1/api/recipe/{}?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e".format(recipe_id))

    u = json.loads(q.text)

    image = u['images'][0]['imageUrlsBySize']['360']
    flavors = u["flavors"]
    ingredients = u["ingredientLines"]
    servings = u["numberOfServings"]
    totaltime = u["totalTime"]
    source = u["source"]["sourceRecipeUrl"]
    name = u["name"]


    # Om like button te veranderen naar unlike indien nodig
    likes_set = liked(session)
    users_set = {}

    #Als sessie bestaat (ofwel ingelogd):
    users = db.execute("SELECT username FROM LIKES WHERE recipe_id = :recipe_id", recipe_id = recipe_id)
    users_set = {user["username"] for user in users }

    return render_template("moreinfo.html", image=image, name=name, flavors=flavors, ingredients=ingredients, servings=servings, totaltime=totaltime, source=source, recipe_id = recipe_id, likes = likes_set, users = users_set)



@app.route("/account", methods=["GET", "POST"])
def account():
    """Account with options to change password and manage favorites of user in session"""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure old password was submitted
        if not request.form.get("Old password"):
            flash("Must provide old password")
            return redirect(url_for("account"))

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username = session["username"])
        print(rows)

        # ensure old password is correct
        if not pwd_context.verify(request.form.get("Old password"), rows[0]["hash"]):
            flash("Invalid password")
            return redirect(url_for("account"))

        # ensure new password is submitted
        elif not request.form.get("New password"):
            flash("Must provide new password")
            return redirect(url_for("account"))

        # password omzetten naar hash
        password = request.form.get("New password")
        password = pwd_context.hash(password)
        print(password)

        #wachtwoord veranderen in database
        rows = db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=session["user_id"], hash= password)
        print(rows)

        # redirect user to home page
        flash("Password changed succesfully")
        return redirect(url_for("account"))

    results = db.execute("SELECT recipe_id, recipe_name, recipe_image FROM likes WHERE id = :id GROUP BY recipe_name", id = session["user_id"])
    likes_set = liked(session)
    return render_template("account.html", results = results, likes = likes_set)


@app.route("/like", methods=['GET','POST'])
def like():
    """Like button"""
    if request.method == "POST":
        # if not session["user_id"]:
        #     return redirect(url_for("login"))
        print("HELP")
        recipe_id = request.get_json()
        recipe_id = recipe_id['fired_button']
        if recipe_id:
            print("Still going strong")
        print(recipe_id)
        print(session["username"])
        s = requests.get("http://api.yummly.com/v1/api/recipe/{}?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e".format(recipe_id))
        y = json.loads(s.text)
        recipe_image = y['images'][0]['imageUrlsBySize']['360']
        recipe_name = y['name']
        result = db.execute("INSERT INTO likes (id, username, recipe_id, recipe_name, recipe_image) VALUES(:id, :username, :recipe_id, :name, :image)",
                                id= session["user_id"], username = session["username"], recipe_id = recipe_id, name = recipe_name, image = recipe_image)
        return render_template("like.html")


@app.route("/unlike", methods=['GET','POST'])
def unlike():
    """Unlike button"""

    if request.method == "POST":
        # if not session["user_id"]:
        #     return redirect(url_for("login"))
        print("HELP")
        recipe_id = request.get_json()
        recipe_id = recipe_id['fired_button']
        if recipe_id:
            print("Still going strong")
        print(recipe_id)
        result = db.execute("DELETE FROM likes WHERE id = :id AND recipe_id = :recipe_id",
                                id= session["user_id"], recipe_id = recipe_id)
        return render_template("unlike.html")