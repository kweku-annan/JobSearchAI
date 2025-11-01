#!/usr/bin/env python
"""Adapter to fetch job listings from ArbeitNow API"""
import requests

from config import Config
from utils.formatters import html_to_text


def fetch_arbeitnow_jobs():
    """Fetches job listings from the ArbeitNow API"""
    try:
        response = requests.get(Config.ARBEITNOW_API_URL, timeout=10)
        response.raise_for_status()
        jobs_data = response.json()
        return jobs_data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ArbeitNow jobs data: {e}")
        return []


def parse_arbeitnow_job():
    """Parse data from ArbeitNow API into standardized job format"""
    jobs = fetch_arbeitnow_jobs()  # Jobs is a list of job dicts
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
        new_job["is_remote"] = job.get('remote', True)
        new_job["location"] = job.get('location', None)
        new_job["job_url"] = job.get('url', None)
        new_job["tags"] = job.get('tags', [])
        parsed_jobs.append(new_job)

    return parsed_jobs

#
# all_jobs = parse_arbeitnow_job()
# print(all_jobs[0])
