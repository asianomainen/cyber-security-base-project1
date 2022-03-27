from flask import flash
from flask.templating import render_template
from db import db


def register(username, hash_value):
    sql = "SELECT username FROM users WHERE LOWER(username)=LOWER(:username)"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user is None:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    else:
        flash("Username is taken. Please choose another username.")
        return render_template("register.html")

    flash("User created. You may now login.")
    return
