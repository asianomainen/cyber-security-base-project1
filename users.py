import hashlib

from flask import session, abort
from db import db
from werkzeug.security import generate_password_hash, check_password_hash


def login(username, password):
    # To fix FLAW 2 remove/comment this line
    hash_value = hashlib.md5(password.encode()).hexdigest()

    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        # Remove/comment this line
        if user.password == hash_value:

        # To fix FLAW 2 uncomment this line
        # if check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["admin"] = False

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
    # To fix FLAW 2 remove/comment this line
    # hash_value = hashlib.md5(password.encode()).hexdigest()

    # To fix FLAW 2 uncomment this line
    hash_value = generate_password_hash(password)

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


def is_admin(user_id):
    sql = "SELECT admin FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    admin = result.fetchone()[0]
    return admin


def remove_account(user_id):
    # id = session["user_id"]
    # if id == user_id:
    #     sql = "DELETE FROM users WHERE id=:user_id"
    #     db.session.execute(sql, {"user_id": user_id})
    #     db.session.commit()
    # else:
    #     abort(403)

    # To fix FLAW 1 remove/comment the 3 rows below and uncomment the code above.
    sql = "DELETE FROM users WHERE id=:user_id"
    db.session.execute(sql, {"user_id": user_id})
    db.session.commit()


def get_account_details(user_id):
    sql = "SELECT username, admin FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    user_details = result.fetchone()
    return user_details
