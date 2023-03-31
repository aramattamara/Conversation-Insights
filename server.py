# System
import json
import os
import time
from threading import Thread
from typing import List

# Import Flask web framework
from flask import Flask, jsonify, render_template, request, flash, redirect
# Import web templating language
from jinja2 import StrictUndefined
# Import werkzeug web framework
from werkzeug.exceptions import abort

import api_calls
# Import crud that handles SQLAlchemy queries
import crud
import export
# Import model.py table definitions
from model import connect_to_db, Member

app = Flask(__name__)

# Required to use Flask session and the debug toolbar
app.secret_key = "dev"

# So that undefined variables in Jinja2 will strike an error vs. failing silently
app.jinja_env.undefined = StrictUndefined

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_EXTENSIONS'] = ['.json']
UPLOAD_FOLDER = 'upload'
# ALLOWED_EXTENSIONS = {'json'}

UPDATE_EVERY_SEC = int(os.environ.get('UPDATE_EVERY_SEC', '60'))


@app.route("/")
def homepage():
    """Show homepage."""
    return render_template("homepage.html")


@app.route("/dashboard/<chat_id>")
def dashboard(chat_id):
    return render_template("dashboard.html", chat_id=chat_id)


@app.route("/start_historical")
def start():
    return render_template("start_historical.html")


@app.route("/start_only_new")
def start_new():
    chats = crud.all_chats()
    return render_template("start_only_new.html", chats=chats)


# ####################### DASHBOARD (SHOWA ALL MEMBERS) ###############
@app.route("/api/get_members.json")
def get_members_json():
    if 'chat_id' not in request.args:
        return "No chat_id query param", 400
    chat_id = request.args['chat_id']
    chat_id = int(chat_id)

    members: List[Member] = crud.get_members(chat_id)
    result_json = []
    for member in members:
        members_d = member.to_dict_with_count()
        result_json.append(members_d)
    return jsonify(result_json)


# ################### DASHBOARD (MEMBER SEARCH) ################### #
@app.route('/search.json', methods=["GET"])
def process_member_search():
    if 'chat_id' not in request.args:
        return "No chat_id query param", 400
    chat_id = request.args['chat_id']
    chat_id = int(chat_id)

    member_search = request.args.get("search-text")
    members = crud.search_members(member_search, chat_id)

    result_json = []
    for member in members:
        result_json.append(member.to_dict_with_count())

    return jsonify(result_json)


@app.route('/api/mes_per_month.json', methods=["GET"])
def mes_per_month():
    selectedIds: List[str] = request.args['selectedIds'].split(',')
    print(selectedIds)

    members_with_agg = crud.mes_per_month_per_user(selectedIds)

    result_dict = {}
    for res in members_with_agg:
        # res_agg = {"cnt": res[0], "month": res[1], "member_id": res[2]}
        # result_dict.append(res_agg)
        res_agg = {"cnt": res[0], "year": res[1], "month": res[2]}
        member_months = result_dict.get(res[3], [])
        result_dict[res[3]] = member_months
        result_dict[res[3]].append(res_agg)

    print(result_dict)
    return jsonify(result_dict)


@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        flash('no file uploaded')
        return

    uploaded_file = request.files['file']
    filename = uploaded_file.filename

    if filename != "":
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
            abort(400)
        # uploaded_file.save(uploaded_file.filename)

    my_dict = json.load(uploaded_file.stream)

    export.export_data_json(my_dict)

    chat_id = my_dict["id"]

    # json.dump(my_dict, '.json')

    return redirect(f'/dashboard/{chat_id}')


def pull_updates_cron():
    print(f'Watching for updates, pull every {UPDATE_EVERY_SEC}s...')
    while t:
        api_calls.pull_new_updates()
        time.sleep(UPDATE_EVERY_SEC)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    app.debug = False

    connect_to_db(app, echo=False)

    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    t = Thread(name="updates-watcher", target=pull_updates_cron, daemon=True)
    t.start()

    app.run(host='0.0.0.0')
