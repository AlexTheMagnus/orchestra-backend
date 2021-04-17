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
    sql = 'DROP TABLE IF EXISTS users;DROP TABLE IF EXISTS watched_movies;DROP TABLE IF EXISTS followed_movies;'
    engine.execute(sql)


def create_user_table():
    db.Table('user', metadata,
             db.Column('user_id', db.String(36),
                       nullable=False, primary_key=True),
             db.Column('username', db.String(255), nullable=False),
             db.Column('avatar', db.String(255), nullable=False)
             )


def create_follow_table():
    db.Table('follow', metadata,
             db.Column('follower', db.String(36),
                       nullable=False, db.ForeignKey("user.user_id"), primary_key=True),
             db.Column('followed', db.String(36),
                       nullable=False, db.ForeignKey("user.user_id"), primary_key=True)
             )


def create_soundtrack_table():
    db.Table('soundtrack', metadata,
             db.Column('soundtrack_id', db.String(36),
                       nullable=False, primary_key=True),
             db.Column('soundtrack_title', db.String(255), nullable=False),
             db.Column('book_isbn', db.String(255), nullable=False),
             db.Column('author', db.String(255), db.ForeignKey(
                 "user.user_id"), nullable=False),
             )


def create_favorite_soundtrack_table():
    db.Table('favorite_soundtrack', metadata,
             db.Column('user_id', db.String(36),
                       nullable=False, primary_key=True),
             db.Column('soundtrack_id', db.Integer(),
                       nullable=False, primary_key=True)
             )


if __name__ == "__main__":
    for engine in engines.values():
        remove_existing_tables(engine)

    create_user_table()
    create_watched_movies_table()
    create_following_movies_table()

    for engine in engines.values():
        metadata.create_all(engine)
