import users
import messages
from app import app

from flask import render_template, request, redirect, session, flash


@app.route("/")
def index():
    message_list = messages.get_list()
    return render_template("index.html", messages=message_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            flash("Wrong username or password")
            return render_template("login.html")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password1"]
        if users.register(username, password):
            if users.login(username, password):
                session["username"] = username
                return redirect("/")
        else:
            flash("Username is taken. Please choose another username.")
            return render_template("register.html")


@app.route("/search")
def search():
    query = request.args["query"]
    messages_found = messages.search(query)
    not_found_or_error = None
    if messages_found[0][0] == "No messages found" or messages_found[0][0] == "ERROR!":
        not_found_or_error = True
    return render_template("search.html", messages=messages_found, not_found_or_error=not_found_or_error)


@app.route("/admin/<int:user_id>", methods=["GET", "POST"])
def admin(user_id):
    if users.is_admin(user_id):
        return render_template("admin.html")
    return render_template("index.html")


@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/send", methods=["POST"])
def send():
    message = request.form["message"]
    if messages.send(message):
        return redirect("/")
    else:
        return render_template("index.html")


@app.route("/account/<int:user_id>")
def account(user_id):
    user_details = users.get_account_details(user_id)
    return render_template("account.html", user_id=user_id, user_details=user_details)


@app.route("/remove_account/<int:user_id>")
def remove_account(user_id):
    users.remove_account(user_id)
    users.logout()
    return redirect("/")
