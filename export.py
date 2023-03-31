import os
import json
from random import choice, randint
from datetime import datetime
import re

import model
from model import Message, Member, Chat, connect_to_db, db
import crud
import server
from flask import Flask


def export_data_json(upload_json=None):
    if upload_json is not None:
        export_data = upload_json
    else:
        with open("result.json") as f:
            export_data = json.loads(f.read())

    chat = Chat(chat_id=export_data["id"], title=export_data["name"])
    db.session.merge(chat)

    messages = []
    members = []
    seen_member_ids = set()

    for message in export_data['messages']:
        print(message)
        if message["type"] != "message":
            continue

        member_id = re.search(r'\d+', message["from_id"])[0]

        first_name = None
        last_name = None
        if message["from"] is None:
            first_name = member_id
            last_name = ""
        else:
            names = message["from"].split(' ')
            first_name = names[0]
            if len(names) > 1:
                last_name = names[1]
            else:
                last_name = ""

        db_member = Member.query.get(member_id)
        if db_member is None:
            member = Member(member_id=member_id,
                            member_name=message.get("username", member_id),
                            first_name=first_name,
                            last_name=last_name,
                            )
        else:
            member = db_member

        if member_id not in seen_member_ids:
            members.append(member)
            seen_member_ids.add(member_id)

        content = []
        for obj in message["text_entities"]:
            content.append(obj["text"])

        message = Message(message_id=message["id"],
                          member_id=member_id,
                          chat_id=chat.chat_id,
                          date=message["date_unixtime"],
                          content=content,
                          )
        messages.append(message)

    db.session.bulk_save_objects(members)

    db.session.bulk_save_objects(messages)

    db.session.commit()


if __name__ == '__main__':
    model.connect_to_db(server.app)
    # model.db.create_all()

    app = Flask(__name__)
    connect_to_db(app)
    # pull_new_updates()

    export_data_json()
