#register
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

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
db = SQL("sqlite:///webik22.db")

@app.route("/")
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
