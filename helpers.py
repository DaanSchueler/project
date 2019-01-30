import csv
import urllib.request
from functools import wraps
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from passlib.apps import custom_app_context as pwd_context

import requests
import json
import pprint as pp
import ctypes

db = SQL("sqlite:///recepts.db")


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def liked (sessie):
     # Om like button te veranderen naar unlike indien nodig
    check = sessie.get("user_id")
    likes_set = {}

    #Als sessie bestaat (ofwel ingelogd):
    if check:
        likes = db.execute("SELECT recipe_id FROM LIKES WHERE id = :id", id= sessie["user_id"])
        likes_set= {like["recipe_id"] for like in likes}

    return likes_set

