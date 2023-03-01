"""CRUD operations. """
from model import db, Message, User, connect_to_db


def create_message():
    message = Message(
    )
    return


def get_users():
    """Return all users."""

    return User.query.all()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
