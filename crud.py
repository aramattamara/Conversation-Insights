"""CRUD operations. """
from typing import List

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


def get_mes_count_by_member(member_id):
    return Message.query.filter_by(member_id=member_id).count()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
