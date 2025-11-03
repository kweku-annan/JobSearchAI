#!/usr/bin/env python
"""Database models design for application"""
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CacheJobData(Base):
    """Defines table for caching job data"""
    __tablename__ = 'cache_job_data'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    job_url = Column(String(255), nullable=True)
    job_description = Column(Text, nullable=False)
    job_title = Column(String(255), nullable=False, index=True)
    company_name = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    date_posted = Column(String(100), nullable=True)
    is_remote = Column(String, default='True', nullable=False)
    fetch_timestamp = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, job_title: str, job_description: str, job_url: str = None,
                 company_name: str = None, location: str = None, date_posted: str = None, is_remote: bool = True):
        """Initializes the CacheJobData instance"""
        self.job_url = job_url
        self.job_description = job_description
        self.job_title = job_title
        self.company_name = company_name
        self.location = location
        self.date_posted = date_posted
        self.is_remote = is_remote

    def to_dict(self):
        """Converts the CacheJobData instance to a dictionary"""
        return {
            'id': self.id,
            'job_url': self.job_url,
            'job_description': self.job_description,
            'job_title': self.job_title,
            'company_name': self.company_name,
            'location': self.location,
            'date_posted': self.date_posted,
            'is_remote': self.is_remote,
            'fetch_timestamp': self.fetch_timestamp.isoformat()
        }