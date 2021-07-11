import os

import sqlalchemy as db
from dotenv import load_dotenv

load_dotenv()

engines = {
    'database': db.create_engine(os.getenv("DB_ENGINE")),
    'test_database': db.create_engine(os.getenv("DB_ENGINE_TEST"))
}

metadata = db.MetaData()


def remove_existing_tables(engine):
    sql = 'DROP TABLE IF EXISTS follow;DROP TABLE IF EXISTS soundtrack;DROP TABLE IF EXISTS favorite;DROP TABLE IF EXISTS likes;DROP TABLE IF EXISTS chapter;'
    engine.execute(sql)


def create_follow_table():
    db.Table('follow', metadata,
             db.Column('follower', db.String(36),
                       nullable=False, primary_key=True),
             db.Column('following', db.String(36),
                       nullable=False, primary_key=True)
             )


def create_soundtrack_table():
    db.Table('soundtrack', metadata,
             db.Column('soundtrack_id', db.String(36),
                       nullable=False, primary_key=True),
             db.Column('book', db.String(255), nullable=False),
             db.Column('soundtrack_title', db.String(255), nullable=False),
             db.Column('author', db.String(36), nullable=False)
             )


def create_favorite_table():
    db.Table('favorite', metadata,
             db.Column('user_id', db.String(36),
                       nullable=False, primary_key=True),
             db.Column('soundtrack_id', db.String(36), db.ForeignKey("soundtrack.soundtrack_id"),
                       nullable=False, primary_key=True)
             )


# This table is called "likes" instead of "like" because "like" is a reserved word
def create_likes_table():
    db.Table('likes', metadata,
             db.Column('user_id', db.String(36),
                       nullable=False, primary_key=True),
             db.Column('soundtrack_id', db.String(36), db.ForeignKey(
                 "soundtrack.soundtrack_id"), nullable=False, primary_key=True)
             )


def create_chapter_table():
    db.Table('chapter', metadata,
             db.Column('chapter_id', db.String(36),
                       nullable=False, primary_key=True),
             db.Column('soundtrack_id', db.String(36), db.ForeignKey(
                 "soundtrack.soundtrack_id"), nullable=False),
             db.Column('number', db.Integer(), nullable=False),
             db.Column('theme', db.String(36), nullable=False),
             db.Column('chapter_title', db.String(255), nullable=True)
             )


if __name__ == "__main__":
    for engine in engines.values():
        remove_existing_tables(engine)

    create_follow_table()
    create_soundtrack_table()
    create_favorite_table()
    create_likes_table()
    create_chapter_table()

    for engine in engines.values():
        metadata.create_all(engine)
