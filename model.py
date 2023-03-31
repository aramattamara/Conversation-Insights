"""Model for telegram analitics app."""
from typing import Dict

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Message(db.Model):
    """A message."""

    __tablename__ = "messages"

    message_id = db.Column(db.Integer, nullable=False, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey("chats.chat_id"), primary_key=True)
    update_id = db.Column(db.Integer, nullable=True)
    member_id = db.Column(db.BigInteger, db.ForeignKey("members.member_id"))
    date = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=True, default="Unknown")

    def __repr__(self):
        return f"<Message message_id={self.message_id} content={self.content} date={self.date}>"


class Member(db.Model, SerializerMixin):
    """A member."""

    __tablename__ = "members"

    member_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    member_name = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    # def __init__(self, member_id: int):
    #     self.member_id = member_id

    def __repr__(self):
        return f"<Member member_id={self.member_id}>"

    def to_dict_with_count(self) -> Dict:
        d = self.to_dict()
        total = Message.query.filter_by(member_id=self.member_id).count()
        d['total'] = total
        return d


class Chat(db.Model):
    """A chat."""

    __tablename__ = "chats"
    chat_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    title = db.Column(db.String)

    def __repr__(self):
        return f"<Chat chat_id{self.chat_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///project", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = flask_app
    db.init_app(flask_app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to the db!")
