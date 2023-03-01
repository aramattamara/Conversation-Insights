from typing import Dict, List

from flask import Flask, jsonify, session, render_template, request, flash, redirect

import crud
from model import Message, connect_to_db, User
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/analytics")
def analytics():

    return render_template("analytics.html")


@app.route("/users.json")
def get_users_json():

    users: List[User] = crud.get_users()
    print(users)

    dd = []
    for u in users:
        d = u.to_dict()
        dd.append(d)

    return jsonify(dd)


@app.route("/users")
def get_users():
    """View all users."""

    users = crud.get_users()

    return render_template("users.html", users=users)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
