"""CRUD operations. """
from datetime import datetime
from typing import List

from sqlalchemy import func, extract, Date, Integer
from model import db, Message, Member, connect_to_db
from sqlalchemy.engine.row import Row


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


def mes_per_day_per_user() -> List[Row]:
    """Function returns total counts per day per user"""
    query = db.session.query(
        func.count().label('cnt'),
        func.to_timestamp(Message.date).cast(Date).label('day'),
        Message.member_id
    ).group_by('day', 'member_id')

    result = query.all()
    return result

#
# def mes_per_month_per_user() -> List[Row]:
#     """Function returns total counts per month per user"""
#     query = db.session.query(
#         func.count().label('cnt'),
#         extract('month', func.to_timestamp(Message.date).cast(Date)).cast(Integer).label("month"),
#         Message.member_id
#     ).group_by('month', 'member_id')
#
#     result = query.all()
#     return result


def mes_per_month_per_user(selectedIds) -> List[Row]:
    """Function returns total counts per month per user"""
    query = db.session.query(
        func.count().label('cnt'),
        extract('year', func.to_timestamp(Message.date).cast(Date)).cast(Integer).label("year"),
        extract('month', func.to_timestamp(Message.date).cast(Date)).cast(Integer).label("month"),
        Message.member_id
    ) .filter(Message.member_id.in_(selectedIds)).group_by('year', 'month', 'member_id')

    result = query.all()
    return result


def mes_per_year_per_user() -> List[Row]:
    """Function returns total counts per year per user"""
    result = db.session.query(
        func.count().label('cnt'),
        extract('year', func.to_timestamp(Message.date).cast(Date)).cast(Integer).label("year"),
        Message.member_id
    ).group_by('year', 'member_id').all()

    return result


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print("Connected to DB.")
