
import os
import json
from random import choice, randint
from datetime import datetime

import model
from model import Message, Member, connect_to_db, db
import crud
import server


model.connect_to_db(server.app)
#model.db.create_all()


def export_data_json():
    with open("result.json") as f:
        export_data = json.loads(f.read())


    for message in export_data['messages']:
        print(message)

        messages = []
        # members = []

        # message = Message(message_id = data)
        #
        # member = Member(member_id = )
        #
        # members.append(member)


if __name__ == '__main__':
    export_data_json()