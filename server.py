import json
from typing import Dict, List

# Import web templating language
from jinja2 import StrictUndefined

# Import Flask web framework
from flask import Flask, jsonify, session, render_template, request, flash, redirect

# Import crud that handles SQLAlchemy queries
import crud

# Import model.py table definitions
from model import Message, connect_to_db, Member

app = Flask(__name__)

# Required to use Flask session and the debug toolbar
app.secret_key = "dev"

# So that undefined variables in Jinja2 will strike an error vs. failing silently
app.jinja_env.undefined = StrictUndefined


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ALLOWED_EXTENSIONS = {'json'}


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/members.json")
def get_members_json():

    members: List[Member] = crud.get_members()

    dd = []
    for member in members:
        d = member.to_dict()
        total = crud.get_mes_count_by_member(member.member_id)
        d['total'] = total
        dd.append(d)

    return jsonify(dd)


@app.route("/users")
def get_users():
    """View all users."""

    users = crud.get_members()

    return render_template("dashboard.html", users=users)


@app.route('/upload')
def handle_upload():
    if 'file' not in request.files:
        flash('no file uploaded')
        return
    export_file = request.files['file']
    my_dict = json.load(export_file.stream)

    return render_template("dashboard.html", my_dict=my_dict)


# ################### DASHBOARD (MEMBER SEARCH) ################### #


@app.route('/search.json', methods=["GET"])
def process_member_search():

    member_search = request.args.get("search-text")

    members = crud.search_members(member_search)

    result_json = []
    for member in members:
        result_json.append(member.to_dict())

    return jsonify(result_json)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
