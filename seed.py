"""Script to seed database."""

import model
import server


# os.system("createdb project")

model.connect_to_db(server.app)

with server.app.app_context():
    # model.db.drop_all()
    model.db.create_all()

    from model import *
    q = Member.query \
        .join(Message, Member.member_id == Message.member_id) \
        .filter(Message.chat_id == 123) \
        .group_by(Member.member_id)

    print(q)