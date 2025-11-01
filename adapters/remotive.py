#!/bin/usr/env python
"""Adapter to fetch remote jobs from Remotive API"""
import requests
from config import Config
from utils.formatters import html_to_text


def fetch_remotive_jobs():
    """Fetches job listings from the Remotive API"""
    try:
        response = requests.get(Config.REMOTIVE_API_URL, timeout=10)
        response.raise_for_status()
        jobs_data = response.json()
        return jobs_data.get('jobs', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Remotive jobs data: {e}")
        return []


def parse_remotive_job():
    """Parse data from Remotive API into standardized job format"""
    jobs = fetch_remotive_jobs()  # Jobs is a list of job dicts
    if not jobs:
        return []

    parsed_jobs = []

    for job in jobs:
        new_job = {}
        new_job["job_title"] = job.get('title', None)
        new_job["company_name"] = job.get('company_name', None)
        description = job.get('description', None)
        if description:
            new_job["job_description"] = html_to_text(description)
        else:
            new_job["job_description"] = job.get('description', None)
        new_job["is_remote"] = job.get('candidate_required_location', None)
        new_job["location"] = job.get('candidate_required_location', None)
        new_job["job_url"] = job.get('url', None)
        new_job["tags"] = job.get('tags', [])
        new_job["date_posted"] = job.get('publication_date', None)
        parsed_jobs.append(new_job)

    return parsed_jobs

