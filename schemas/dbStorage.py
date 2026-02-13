#!/usr/bin/env python
"""Database Storage Operations using SQLite and SQLAlchemy"""
import re

from sqlalchemy import create_engine, Integer, func, cast, and_, or_, case
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
        """
        1. Normalize the text
        2. Partial Matching
        3. Multi-word handling (user intent)
        4. Relevance Ranking
            => If 100 hundred jobs match, which appears first?
            a. Exact match > partial match
            b. Position of match: Title starts with search term > title contains search term
            c. Word order preservation: "Software Engineer" ranks higher than "Engineer, Softwaree"
            d. Length: Shorter titles (less noise) rank higher
            e. Completeness: All search terms present > some terms present.
        5. Fuzzy Tolerance (typos & variations)
            a. "enginer" -> should still find "engineer"
            b. "dev" -> should find "developer", "devops", "dev engineer"
        """
        normalized_title = self.normalize_for_storage(job_title)
        if not normalized_title:
            return []

        # Split into individual words
        search_terms = normalized_title.split()
        if len(search_terms) > 1:
            word_conditions = [
                func.lower(CacheJobData.job_title).like(f'%{term}%')
                for term in search_terms
            ]
            base_filter = and_(*word_conditions)
        else:
            base_filter = func.lower(CacheJobData.job_title).like(f'%{normalized_title}%')


        # Calculate relevance score based on multiple factors
        relevance_score = case(
            # Exact match
            (func.lower(CacheJobData.job_title) == normalized_title, 4),
            # Starts with search term
            (func.lower(CacheJobData.job_title).like(f'{normalized_title}%'), 3),
            # Contains search term
            (func.lower(CacheJobData.job_title).like(f'%{normalized_title}%'), 2),
            # All words present in orderr (with words between)
            *self._build_word_order_conditions(search_terms, score=1),
            # Otherwise = 0 (won't match WHERE clause anyway)
            else_=0
        )
        results = (
            self.__session.query(CacheJobData)
            .filter(base_filter)
            .order_by(
                relevance_score.desc(),
                func.length(CacheJobData.job_title),  # Shorter titles rank higher
                CacheJobData.job_title  # Alphabetical order as tiebreaker
            ).all()
        )

        # TODO: Add fuzzy matching logic here (e.g., using Levenshtein distance or similar)
        if not results:
            results = self._fuzzy_search(normalized_title, search_terms)
        return results




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

    # @staticmethod
    def _build_word_order_conditions(self, search_terms, score):
        """Helper to check if words appear in original order"""
        if len(search_terms) < 2:
            return []

        # Build a pattern like %software%engineer% to check word order
        pattern = '%'.join(search_terms)
        pattern = f'%{pattern}%'
        return [(func.lower(CacheJobData.job_title).like(pattern), score)]

    def _fuzzy_search(self, normalized_title, search_terms):
        """Fallback fuzzy search when exact matching fails"""
        from fuzzywuzzy import fuzz
        all_jobs = self.__session.query(CacheJobData).all()

        # Calculate fuzzy score for each job
        scored_jobs = []
        for job in all_jobs:
            job_title_lower = job.job_title.lower()

            # Calculate similarity score (0-100)
            similarity = fuzz.partial_ratio(normalized_title, job_title_lower)

            # Only include if similarity is above threshold (e.g., 70)
            if similarity >= 70:
                scored_jobs.append((job, similarity))

        # Sort by similarity score (highest first
        scored_jobs.sort(key=lambda x: x[1], reverse=True)

        # Return just the job objects (without scores)
        return  [job for job, score in scored_jobs]



    @staticmethod
    def normalize_for_storage(text):
        """Normalizes text for consistent storage"""
        if not text:
            return text
        normalized = text.lower().strip()

        # Filter out very common/generic words that don't help matching
        stop_words = {'and', 'or', 'the', 'a', 'an', 'in', 'at', 'for', 'with', 'remote', 'hybrid'}
        words = normalized.split()
        meaningful_words = [w for w in words if w not in stop_words and len(w) > 1]
        normalized = ' '.join(meaningful_words)

        # Remove special characters but keep spaces and hyphens
        normalized = re.sub(r'[^\w\s-]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized











