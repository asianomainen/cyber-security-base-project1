from os import getenv

from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["FLASK_ENV"] = getenv("FLASK_ENV")

import routes
