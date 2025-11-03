#!/usr/bin/env python
"""
 -- cache_logic.py --
    Logic for caching data in the application
    1. Check if there is data in the cache
    2. If not, fetch from external APIs and store in cache
    3. If there is data, check if it's stale
    4. If stale, refresh the cache
    5. If not stale, return the cached data by the value demanded
"""

from datetime import datetime, timedelta, UTC

from adapters.adapter_logic import aggregate_job_listings
from schemas.dbStorage import DBStorage
from models.cache_job_data import CacheJobData

def save_to_cache():
    """Saves new job data to the cache"""
    db_storage = DBStorage()
    new_jobs = aggregate_job_listings()
    for job in new_jobs:
        job_title = db_storage.normalize_for_storage(job.get('job_title'))
        job_entry = CacheJobData(
            job_title=job_title,
            job_description=job.get('job_description'),
            job_url=job.get('job_url'),
            company_name=job.get('company_name'),
            location=job.get('location'),
            date_posted=job.get('date_posted'),
            is_remote=job.get('is_remote', True)
        )
        db_storage.save(job_entry)


def caching_logic():
    """Logic to manage caching of job data"""
    db_storage = DBStorage()
    now = datetime.now(UTC)

    # Check if there is any data in the cache
    if not db_storage.check_for_data():
        # Fetch data from external APIs and store in cache
        save_to_cache()
    # There is data, check if it's stale
    else:
        # Get the timestamp of the most recent cache entry
        last_entry = db_storage.fetch_last_refreshed()
        if now - last_entry > timedelta(hours=24):
            db_storage.delete_all()
            save_to_cache()


def get_cached_jobs_by_title(job_title):
    """Retrieves cached job data by job title"""
    db_storage = DBStorage()
    cached_jobs = db_storage.get_by_title(job_title)
    return cached_jobs



