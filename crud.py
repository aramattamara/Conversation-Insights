"""CRUD operations. """
from datetime import datetime
from typing import List
from sqlalchemy import func
from sqlalchemy import Date
from model import db, Message, Member, connect_to_db


def get_members():
    """Return all users."""
    return Member.query.all()


def search_members(search_value) -> List[Member]:
    """Checks if member exists in DB. If so returns instantiated Member (User) object.
    Returns none if member not found"""
    return Member.query.filter((Member.first_name.like(f'%{search_value}%')) |
                               (Member.last_name.like(f'%{search_value}%')) |
                               (Member.member_name.like(f'%{search_value}%'))).all()


def get_msg() -> List[Message]:
    """Return all users."""
    return Message.query.all()


def mes_per_day_per_user():
    """Function returns total counts per user per day"""
    query = db.session.query(
        func.count().label('cnt'),
        func.to_timestamp(Message.date).cast(Date).label('day'),
        Message.member_id
    ).group_by('day', 'member_id')

    result = query.all()
    return result


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print("Connected to DB.")
