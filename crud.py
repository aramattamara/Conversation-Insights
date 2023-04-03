"""CRUD operations. """
from typing import List, Tuple, Dict

import sqlalchemy
from sqlalchemy import func, extract, Date, Integer
from model import db, Message, Member, Chat, connect_to_db
from sqlalchemy.engine.row import Row


def get_members(chat_id: int):
    """Return all users where chat_id eql selected chat_id."""
    return Member.query \
        .join(Message, Member.member_id == Message.member_id) \
        .filter(Message.chat_id == chat_id) \
        .group_by(Member.member_id) \
        .all()


def total_members(chat_id: int):
    return Member.query \
        .join(Message, Member.member_id == Message.member_id) \
        .filter(Message.chat_id == chat_id) \
        .group_by(Member.member_id) \
        .count()


def all_chats():
    return Chat.query.all()


def search_members(search_value: str, chat_id: int) -> List[Member]:
    return Member.query \
        .join(Message, Member.member_id == Message.member_id) \
        .filter(Message.chat_id == chat_id) \
        .filter(
        (Member.first_name.ilike(f'%{search_value}%')) |
        (Member.last_name.ilike(f'%{search_value}%')) |
        (Member.member_name.ilike(f'%{search_value}%'))) \
        .group_by(Member.member_id) \
        .all()


def search_members_with_messages_count(search_value: str, chat_id: int) -> List[Dict]:
    return db.session.query(Member, func.count().label('total')) \
        .join(Message, Member.member_id == Message.member_id) \
        .filter(Message.chat_id == chat_id) \
        .filter(
            (Member.first_name.ilike(f'%{search_value}%')) |
            (Member.last_name.ilike(f'%{search_value}%')) |
            (Member.member_name.ilike(f'%{search_value}%'))) \
        .group_by(Member.member_id) \
        .order_by(sqlalchemy.desc('total')) \
        .all()


# def get_msg() -> List[Message]:
#     """Return all users."""
#     return Message.query.all()


def mes_per_day_per_user(chat_id: int) -> List[Row]:
    """Function returns total counts per day per user"""
    query = db.session \
        .join(Message, Member.member_id == Message.member_id) \
        .filter(Message.chat_id == chat_id) \
        .query(func.count().label('cnt'), func.to_timestamp(Message.date).cast(Date).label('day'), Message.member_id) \
        .group_by('day', 'member_id')

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


def mes_per_month_per_user(selected_ids: List[int], chat_id: int) -> List[Row]:
    """Function returns total counts per month per user"""
    query = (db.session.query(
        func.count().label('cnt'),
        extract('year', func.to_timestamp(Message.date).cast(Date)).cast(Integer).label("year"),
        extract('month', func.to_timestamp(Message.date).cast(Date)).cast(Integer).label("month"),
        Message.member_id
    )
             .filter(Message.member_id.in_(selected_ids))
             .group_by('year', 'month', 'member_id')
             .order_by('year', 'month', 'member_id')
             )

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
    search_members_with_messages_count('val', 1420590782)
