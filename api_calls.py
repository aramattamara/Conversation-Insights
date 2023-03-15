# To Access OS environmental variables
import os
from typing import Dict

from flask import Flask
# Library for API calls
import requests

from model import Message, Member, connect_to_db, db

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
    messages = []
    members = []
    chat = []
    for i in data["result"]:
        print(i)
        if "message" not in i:
            continue
        if "text" not in i["message"]:
            continue

        message_from = i["message"]["from"]
        member = Member(member_id=message_from["id"],
                        member_name=message_from["username"],
                        first_name=message_from.get("first_name", None),
                        last_name=message_from.get("last_name", None)
                        )
        members.append(member)

        # c = Chat(chat_id=i["message"]["chat"]["id"])
        # chat.append(c)

        message = Message(update_id=i["update_id"],
                          message_id=i["message"]["message_id"],
                          member_id=message_from["id"],
                          date=i["message"]["date"],
                          content=i["message"]["text"]
                          )
        messages.append(message)

    # Users and chats must be saved first, as Message has foreight keys to them
    for member in members:
        db.session.merge(member)

    for c in chat:
        db.session.merge(c)

    for message in messages:
        db.session.merge(message)

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
