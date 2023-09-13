"""Model for telegram analytics app."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class User(db.Model):
    """A user."""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class UserChat(db.Model):
    """An N:N relationship between Chat and User."""
    __tablename__ = "user_chat"
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey("chats.chat_id"), nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default="NOW()")


class Chat(db.Model):
    """A chat."""

    __tablename__ = "chats"
    chat_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    title = db.Column(db.String)

    def __repr__(self):
        return f"<Chat chat_id{self.chat_id}>"


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

    def to_dict_with_count(self, chat_id: int) -> dict:
        d = self.to_dict()
        total = Message.query.filter_by(member_id=self.member_id, chat_id=chat_id).count()
        d['total'] = total
        return d


# ############################ TESTING AND DB CONNECTIONS ########################
#
def connect_to_db(flask_app, db_uri="postgresql:///project", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = flask_app
    db.init_app(flask_app)
#
#
# def example_data():
#     """Example data for test database."""
#
#     ph = PasswordHasher()
#
#     testuser = User(user_id=10, name="Marta", email="marta2@test.com", password=ph.hash("test"))
#     testmessage = BinType(type_code="R")
#     testmember = Record(record_id=100, user_id=testuser.user_id, bin_type_code="R", weight=5, date_time=date(2022,11,18))
#
#     db.session.add(testuser)
#     db.session.add(testmessage)
#     db.session.add(testmember)
#     db.session.commit()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to the db!")
