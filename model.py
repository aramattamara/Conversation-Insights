"""Model for telegram analitics app."""
from typing import Dict

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Message(db.Model):
    """A message."""

    __tablename__ = "messages"

    update_id = db.Column(db.Integer, nullable=False, primary_key=True)
    message_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # chat_id = db.Column(db.Integer, db.ForeignKey("chats.chat_id"))
    date = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=False, default="Unknown")

    def __repr__(self):
        return f"<Message message_id={self.message_id} content={self.content} date={self.date}>"


class User(db.Model, SerializerMixin):
    """A user."""

    __tablename__ = "users"
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    username = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id}>"


# class Chat(db.Model):
#     """A chat."""
#
#     __tablename__ = "chats"
#     chat_id = db.Column(db.BigInteger, nullable=False, primary_key=True,)
#    # title = db.Column(db.String)
#
#     def __repr__(self):
#         return f"<Chat chat_id{self.chat_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///project", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
