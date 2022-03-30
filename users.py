import hashlib

from flask import session
from db import db


def login(username, password):
    hash_value = hashlib.md5(password.encode()).hexdigest()
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if user.password == hash_value:
            session["user_id"] = user.id
            session["admin"] = False
            session["csrf_token"] = user.id

            if is_admin(user.id):
                session["admin"] = True
            return True
        else:
            return False


def logout():
    try:
        del session["username"]
    except:
        return


def register(username, password):
    hash_value = hashlib.md5(password.encode()).hexdigest()
    sql = "SELECT username FROM users WHERE LOWER(username)=LOWER(:username)"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user is None:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
        return True
    else:
        return False


def user_id():
    return session.get("user_id", 0)


def is_admin(user_id):
    sql = "SELECT admin FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    admin = result.fetchone()[0]
    return admin


def remove_account(user_id):
    sql = "DELETE FROM users WHERE id=:user_id"
    db.session.execute(sql, {"user_id": user_id})
    db.session.commit()
