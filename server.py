from flask import Flask, session, render_template, request, flash, redirect
from model import Message, connect_to_db
import os
import requests
import json

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")




if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
