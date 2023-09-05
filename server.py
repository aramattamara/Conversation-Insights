# Server for conversation insights app
from flask import Flask, jsonify, render_template, request, session, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, Member, Chat
from argon2 import PasswordHasher
from jinja2 import StrictUndefined
from typing import List, Dict
from werkzeug.exceptions import abort
from threading import Thread

import json
import os
import time
import api_calls
import crud
import model
import export

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
ph = PasswordHasher()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_EXTENSIONS'] = ['.json']
app.config['UPLOAD_FOLDER'] = 'upload'

# Use the DebugToolbar
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True
app.config["DEBUG_TB_PROFILER_ENABLED"] = True
DebugToolbarExtension(app)

UPDATE_EVERY_SEC = int(os.environ.get('UPDATE_EVERY_SEC', '60'))

connect_to_db(app, echo=True)


####################### HOMEPAGE/LOGIN/LOGOUT/REGISTER ##############################
@app.route("/")
def homepage():
    """View homepage."""
    session_user_id = session.get("user_id")

    if session_user_id:
        return redirect("/profile")

    return render_template("homepage.html")


@app.route("/register", methods=["POST"])
def register_user():
    """Register a new user."""

    user_email = request.form.get("email")
    user_password = request.form.get("password")
    user_name = request.form.get("name")

    # check that user does not exist in db
    user = crud.get_user_by_email(user_email)

    # if user exist in db, tell them to login
    if user:
        flash("That email already exist, try logging in")
        return redirect("/")

    # if user does not exist in db yet, add and commit their info to db
    else:
        # but first check if they entered a password
        if not user_password:
            flash("Please enter in a password")
            return redirect("/")
        else:
            hashed_pw = ph.hash(user_password)
            new_user = crud.create_user(user_email, hashed_pw, user_name)
            model.db.session.add(new_user)
            model.db.session.commit()


@app.route("/login", methods=["POST"])
def login():
    """Process user login."""

    # get user email and password from Login form
    user_email = request.form.get("email")
    password = request.form.get("password")

    # query db for user, if no user will return None, if user will return user object
    user = crud.get_user_by_email(user_email)

    # if query returns None, redirect to try signing in again
    if not user:
        flash("That email does not exist!")
        return redirect('/')

    # if user in db, check that their password is correct
    else:
        try:
            ph.verify(user.password, password)
        except:
            flash(f"{user.email}, check your password")
            return redirect("/")

        # if their password is correct, store their user_id in session
        session["user_id"] = user.user_id

        # welcome them back using their email from the Loging Form
        flash(f"Welcome back, {user.name}!")

        # take them to their profile page with ID from session
        return redirect("/profile")


@app.route("/profile/logout")
def user_logout():
    """Process user logout."""

    session.clear()

    return redirect("/")


##################### User Profile Routes ############################################
@app.route("/profile")
def user_profile():
    # """Show user's profile page."""

    # getting the user's user_id from session, returns None if no user_id
    session_user_id = session.get("user_id")

    # if there is no user_id in the session, ask the user to Login
    if not session_user_id:
        flash("Please Login")
        return redirect("/")

    # querying the db with the user_id stored in session
    user = crud.get_user_by_id(session_user_id)

    # returns a list of the user's chats

    return render_template("profile.html", user=user)


@app.route("/dashboard/<chat_id>")
def dashboard(chat_id):
    chat: Chat = crud.get_chat(chat_id)
    total_members = crud.total_members(chat_id)
    if chat is None:
        return "No such chat_id: " + chat_id, 400
    return render_template("dashboard.html", chat_id=chat_id, chat_title=chat.title, total_members=total_members)


@app.route("/start_historical")
def start():
    return render_template("start_historical.html")


@app.route("/start_only_new")
def start_new():
    chats = crud.all_chats_with_total_members()
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
        members_d = member.to_dict_with_count(chat_id)
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
    rows: List[Dict] = crud.search_members_with_messages_count(member_search, chat_id)
    # rows: List[Member] = crud.search_members(member_search, chat_id)

    result: List[Dict] = []
    for row in rows:
        # result_json.append(row.to_dict_with_count(chat_id))

        member_dict: Dict = {
            "first_name": row['Member'].first_name,
            "last_name": row['Member'].last_name,
            "member_id": row['Member'].member_id,
            "member_name": row['Member'].member_name,
            "total": row['total'],
        }
        result.append(member_dict)

    return jsonify(result)


@app.route('/api/mes_per_month.json', methods=["GET"])
def mes_per_month():
    if 'chat_id' not in request.args:
        return "No chat_id query param", 400
    chat_id = request.args['chat_id']
    chat_id = int(chat_id)

    selected_ids: List[str] = request.args['selectedIds'].split(',')
    selected_ids: List[int] = [int(sel_id) for sel_id in selected_ids]
    # print(selected_ids)

    members_with_agg = crud.mes_per_month_per_user(selected_ids, chat_id)

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
    t = Thread(name="updates-watcher", target=pull_updates_cron, daemon=True)
    t.start()

    app.run(host='0.0.0.0')
