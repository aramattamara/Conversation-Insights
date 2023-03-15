import json
from typing import List

# Import web templating language
from jinja2 import StrictUndefined

# Import Flask web framework
from flask import Flask, jsonify, render_template, request, flash

# Import crud that handles SQLAlchemy queries
import crud

# Import model.py table definitions
from model import connect_to_db, Member

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


# ####################### DASHBOARD (SHOWA ALL MEMBERS) ###############
@app.route("/api/get_members.json")
def get_members_json():
    members: List[Member] = crud.get_members()
    result_json = []
    for member in members:
        members_d = member.to_dict_with_count()
        result_json.append(members_d)
    return jsonify(result_json)


# ################### DASHBOARD (MEMBER SEARCH) ################### #
@app.route('/search.json', methods=["GET"])
def process_member_search():
    member_search = request.args.get("search-text")
    members = crud.search_members(member_search)

    result_json = []
    for member in members:
        result_json.append(member.to_dict_with_count())

    return jsonify(result_json)


@app.route('/api/mes_per_month.json', methods=["GET"])
def mes_per_month():
    members_with_agg = crud.mes_per_month_per_user()

    result_dict = {}
    for res in members_with_agg:
        # res_agg = {"cnt": res[0], "month": res[1], "member_id": res[2]}
        # result_dict.append(res_agg)
        res_agg = {"cnt": res[0], "year-month": f'{res[1]}-{res[2]}'}
        member_months = result_dict.get(res[3], [])
        result_dict[res[3]] = member_months
        result_dict[res[3]].append(res_agg)

    print(result_dict)
    return jsonify(result_dict)


@app.route('/upload')
def handle_upload():
    if 'file' not in request.files:
        flash('no file uploaded')
        return
    export_file = request.files['file']
    my_dict = json.load(export_file.stream)

    return render_template("dashboard.html", my_dict=my_dict)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
