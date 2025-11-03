#!/usr/bin/env python
"""Database Storage Operations using SQLite and SQLAlchemy"""
import re

from sqlalchemy import create_engine, Integer, func, cast, and_, or_
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
        try:
            search_terms = self._extract_search_terms(job_title)

            if not search_terms:
                return []
            query = self.__session.query(CacheJobData)

            conditions = []
            for term in search_terms:
                conditions.append(
                    CacheJobData.job_title.like(f'%{term}%')
                )
            query = query.filter(and_(*conditions))
            query = query.order_by(CacheJobData.fetch_timestamp.desc())
            jobs = query.first()
            if jobs:
                return jobs
            query = query.filter(or_(*conditions))
            query = query.order_by(CacheJobData.fetch_timestamp.desc())
            jobs = query.first()
            return jobs
        except Exception as e:
            return []


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

    def _extract_search_terms(self, job_title):
        """Extracts meaningful search terms"""
        if not job_title:
            return []
        title_lower = job_title.lower().strip()
        tech_roles = [
            'software engineer', 'software developer',
            'backend developer', 'backend engineer',
            'frontend developer', 'frontend engineer',
            'full stack', 'fullstack',
            'data scientist', 'data analyst', 'data engineer',
            'machine learning', 'ml engineer',
            'devops engineer', 'devops',
            'site reliability', 'sre',
            'cloud engineer', 'cloud architect',
            'security engineer', 'cybersecurity',
            'mobile developer', 'ios developer', 'android developer',
            'web developer', 'web designer',
            'ui designer', 'ux designer', 'product designer',
            'qa engineer', 'test engineer',
            'database administrator', 'dba',
        ]

        matched_roles = []
        for role in tech_roles:
            if role in title_lower:
                matched_roles.append(role)
                title_lower = title_lower.replace(role, '').strip()

        remaining_words = title_lower.split()

        # Filter out very common/generic words that don't help matching
        stop_words = {'and', 'or', 'the', 'a', 'an', 'in', 'at', 'for', 'with', 'remote', 'hybrid'}
        meaningful_words = [w for w in remaining_words if w not in stop_words and len(w) > 1]

        search_terms = matched_roles + meaningful_words

        seen = set()
        unique_terms = []
        for term in search_terms:
            if term not in seen:
                seen.add(term)
                unique_terms.append(term)

        return unique_terms

    def normalize_for_storage(self, text):
        """Normalizes text for consistent storage"""
        if not text:
            return text
        normalized = text.lower().strip()

        # Remove special characters but keep spaces and hyphens
        normalized = re.sub(r'[^\w\s-]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized






