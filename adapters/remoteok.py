#!/usr/bin/env python
"""Adapter to fetch job listings from """

import requests
from config import Config
from utils.formatters import html_to_text

def fetch_remoteok_jobs():
    """Fetches job listings from the RemoteOK API"""
    try:
        response = requests.get(Config.REMOTEOK_API_URL, timeout=10)
        response.raise_for_status()
        jobs_data = response.json()
        return jobs_data[1:]  # The first element is metadata
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RemoteOK jobs data: {e}")
        return []


def parse_remoteok_job():
    """Parse data from RemoteOK API into standardized job format"""
    jobs = fetch_remoteok_jobs()  # Jobs is a list of job dicts
    if not jobs:
        return []

    parsed_jobs = []

    for job in jobs:
        new_job = {}
        new_job["job_title"] = job.get('position', None)
        new_job["company_name"] = job.get('company', None)
        description = job.get('description', None)
        if description:
            new_job["job_description"] = html_to_text(description)
        else:
            new_job["job_description"] = job.get('description', None)
        new_job["is_remote"] = job.get('remote', True)
        new_job["location"] = job.get('location', None)
        new_job["job_url"] = job.get('url', None)
        new_job["tags"] = job.get('tags', [])
        new_job["date_posted"] = job.get('date', None)
        parsed_jobs.append(new_job)

    return parsed_jobs