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



import pprint as pp

# t = requests.get("http://api.yummly.com/v1/api/recipes?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e")
# x = json.loads(t.text)
# for i in x['matches']:
#     recipe_id = i['id']
#     recipe_name = i['recipeName']


#     s = requests.get("http://api.yummly.com/v1/api/recipe/{}?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e".format(recipe_id))
#     y = json.loads(s.text)
#     recipe_image = y['images'][0]['imageUrlsBySize']['360']

#     result = db.execute("INSERT INTO likes (id, recipe_id, recipe_name, recipe_image) VALUES(:id, :recipe_id, :name, :image)",
#                             id = 333 , recipe_id = recipe_id, name = recipe_name, image = recipe_image)



@app.route("/")
@app.route("/index")
def index():

    results = db.execute("SELECT recipe_id, recipe_name, recipe_image, count(recipe_name) AS total FROM likes GROUP BY recipe_name ORDER BY total DESC ")
    # print (results)

#     SELECT product_id, count(*) AS total
# FROM order_line
# GROUP BY product_id
# ORDER BY total

    return render_template("index.html", results = results)


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


        return render_template("results.html", recepten=recepten, all_checked=all_checked)

    else:
        return render_template("search.html")

@app.route("/moreinfo", methods=["GET", "POST"])
def moreinfo():
    recipe_id = request.args.get('id')
    recipe_id = recipe_id[1:]
    print(recipe_id)

    q = requests.get("http://api.yummly.com/v1/api/recipe/{}?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e".format(recipe_id))

    u = json.loads(q.text)

    pp.pprint(u)

    image = u['images'][0]['imageUrlsBySize']['360']
    flavors = u["flavors"]
    ingredients = u["ingredientLines"]
    servings = u["numberOfServings"]
    kcal = u["nutritionEstimates"][14]["value"]
    prot_grams = u["nutritionEstimates"][25]["value"]
    totaltime = u["totalTime"]
    source = u["source"]["sourceRecipeUrl"]
    name = u["name"]

    return render_template("moreinfo.html", image=image, name=name, flavors=flavors, ingredients=ingredients, servings=servings, kcal=kcal, prot_grams=prot_grams, totaltime=totaltime, source=source)




@app.route("/account", methods=["GET", "POST"])
def account():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure old password was submitted
        if not request.form.get("Old password"):
            return ("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure old password is correct
        if not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # ensure password confirmation was submitted
        elif not request.form.get("New password"):
            return ("must provide password")

        # password omzetten naar hash
        password = request.form.get("New password")
        password = pwd_context.hash(password)

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # als de gebruikersnaam al bestaat
        if not user:
            return ("username wrong")

        # onthou dat de gebruiker ingelogd is
        session["user_id"] = user

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("account.html")

@app.route("/test", methods=['GET','POST'])
def test():
    if request.method == "POST":
        # if not session["user_id"]:
        #     return redirect(url_for("login"))
        print("HELP")
        recipe_id = request.get_json()
        recipe_id = recipe_id['fired_button']
        if recipe_id:
            print("Still going strong")
        print(recipe_id)
        s = requests.get("http://api.yummly.com/v1/api/recipe/{}?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e".format(recipe_id))
        y = json.loads(s.text)
        recipe_image = y['images'][0]['imageUrlsBySize']['360']
        recipe_name = y['name']
        result = db.execute("INSERT INTO likes (id, recipe_id, recipe_name, recipe_image) VALUES(:id, :recipe_id, :name, :image)",
                                id= session["user_id"], recipe_id = recipe_id, name = recipe_name, image = recipe_image)
        return render_template("test.html")



@app.route("/unlike", methods=['GET','POST'])
def unlike():
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
        return render_template("test.html")
   


