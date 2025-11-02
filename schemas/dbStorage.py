#!/usr/bin/env python
"""Database Storage Operations using SQLite and SQLAlchemy"""
from sqlalchemy import create_engine, Integer, func, cast
from sqlalchemy.orm import sessionmaker, scoped_session

from models.cache_job_data import Base, CacheJobData

class DBStorage:
    """Manages storage of SQLAlchemy database operations"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine and session"""
        self.__engine = create_engine('sqlite:///cache_job_data.db', pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def save(self, obj):
        """Saves an object to the database"""
        try:
            self.__session.add(obj)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def exists(self, job_title):
        """Checks if a CacheJobData with the given job title exists"""
        return self.__session.query(CacheJobData).filter_by(job_title=job_title).first()

    def get_by_title(self, job_title):
        """Retrieves a CacheJobData by its job title"""
        return self.__session.query(CacheJobData).filter_by(job_title=job_title).order_by(func.random()).limit(5).all()

    def delete_all(self):
        """Deletes all records from the CacheJobData table"""
        try:
            num_rows_deleted = self.__session.query(CacheJobData).delete()
            self.__session.commit()
            return num_rows_deleted
        except Exception as e:
            self.__session.rollback()
            raise e

    def check_for_data(self):
        """Checks if there is any data in the CacheJobData table"""
        return self.__session.query(CacheJobData).first() is not None

    def fetch_last_refreshed(self):
        """Fetches the timestamp of one of the entries"""
        last_refreshed = self.__session.query(CacheJobData).order_by(CacheJobData.fetch_timestamp.desc()).first()
        fetch_last_timestamp = last_refreshed.fetch_timestamp if last_refreshed else None
        return fetch_last_timestamp





