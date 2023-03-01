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


def save_data(data: Dict):

    mes = []
    usr = []
    chat = []
    for i in data["result"]:
        print(i)
        if "message" not in i:
            continue
        if "text" not in i["message"]:
            continue

        u = User(user_id=i["message"]["from"]["id"],
                 first_name=i["message"]["from"]["first_name"],
                 last_name=i["message"]["from"]["last_name"],
                 username=i["message"]["from"]["username"])
        usr.append(u)

        # c = Chat(chat_id=i["message"]["chat"]["id"])
        # chat.append(c)

        m = Message(update_id=i["update_id"],
                    message_id=i["message"]["message_id"],
                    date=i["message"]["date"],
                    content=i["message"]["text"]
                    )
        mes.append(m)

    # Users and chats must be saved first, as Message has foreight keys to them
    db.session.add_all(usr)
    db.session.add_all(chat)
    db.session.add_all(mes)
    db.session.commit()


def pull_new_updates():
    data = get_updates()
    save_data(data)

# import schedule
# if __name__ == '__main__':
    # # schedule.every(30).seconds.do(get_text)
    # while True:
    #     # schedule.run_pending()
    #     get_text()
    #     sleep(30)


app = Flask(__name__)
connect_to_db(app)
pull_new_updates()

