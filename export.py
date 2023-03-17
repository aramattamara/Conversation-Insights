
import os
import json
from random import choice, randint
from datetime import datetime

from model import Message, Member, connect_to_db, db,
import crud
import server


model.connect_to_db(server.app)
model.db.create_all()


with open("export.json") as f:
export_data = json.loads(f.read())


def export_data_json():

        for data in export_data:



            messages = []
            members = []

            message = Message(message_id = )

            member = Member(member_id = )

            members.append(member)


