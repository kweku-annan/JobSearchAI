#!/usr/bin/env python
"""Database models design for application"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CacheJobData(Base):
    """Defines table for caching job data"""
    __tablename__ = 'cache_job_data'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    job_url = Column(String(255), nullable=True)
    job_description = Column(Text, nullable=False)
    job_title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    date_posted = Column(String(100), nullable=True)
    fetch_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, job_title: str, job_description: str, job_url: str = None,
                 company_name: str = None, location: str = None, date_posted: str = None):
        """Initializes the CacheJobData instance"""
        self.job_url = job_url
        self.job_description = job_description
        self.job_title = job_title
        self.company_name = company_name
        self.location = location
        self.date_posted = date_posted
