import hashlib

import users
from app import app

from flask import render_template, request, redirect, session

from db import db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password1"]
        hash_value = hashlib.md5(password.encode()).hexdigest()
        users.register(username, hash_value)
        return redirect("/")


@app.route("/result")
def result():
    query = request.args["query"]
    sql = "SELECT username FROM users WHERE username=\'" + query + "\'"
    try:
        query_result = db.session.execute(sql, {"query": query})
        users_found = query_result.fetchall()
        if len(users_found) == 0:
            not_found_message = [("User not found",), ]
            return render_template("result.html", users=not_found_message)
        return render_template("result.html", users=users_found)
    except:
        error_message = [("ERROR!",), ]
        return render_template("result.html", users=error_message)


@app.route("/admin")
def admin():
    return render_template("index.html")

# @app.route("/send", methods=["POST"])
# def send():
#     content = request.form["content"]
#     db.session.execute("INSERT INTO messages (content) VALUES (\'" + content + "\')")
#     db.session.commit()
#     return redirect("/")

#     passwrd = "password"
#     hashed = hashlib.md5(passwrd.encode())
#     return render_template("index.html", password=hashed.hexdigest())

#     sql = "SELECT username FROM users WHERE username LIKE \'%" + query + "%\'"
