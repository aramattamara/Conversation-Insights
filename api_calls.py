#To Access OS environmental variables
import os
from typing import Dict

from flask import Flask
# Library for API calls
import requests
import json
from model import Message, User, connect_to_db, db

bot_key = os.environ['API_BOT_KEY']


def get_updates() -> Dict:
    response = requests.get('https://api.telegram.org/bot' + bot_key + '/getUpdates')
    print(response.text)
    return response.json()


def example_data():
    mes = [
        Message(content="hello", chat="blue", date="2022-02-13 12:10:15"),
        Message(content="hi", chat="red", date="2008-11-11 11:12:01")
    ]

    db.session.add_all(mes)
    db.session.commit()


def get_text():
    text = get_updates()
    mes = []
    for i in text["result"]:
        m = Message(content=i["message"]['text'], date=i['date'])
        mes.append(m)
    db.session.add_all(mes)
    db.session.commit()



# import schedule
# if __name__ == '__main__':
    # # schedule.every(30).seconds.do(get_text)
    # while True:
    #     # schedule.run_pending()
    #     get_text()
    #     sleep(30)

app = Flask(__name__)
connect_to_db(app)
get_updates()

