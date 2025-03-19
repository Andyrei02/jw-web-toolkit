from flask import Blueprint, render_template, redirect, url_for
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    return render_template("login.html")
