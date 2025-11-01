#!/usr/bin/env python
"""Adapter to fetch job listings from JobIcy"""
import requests
from config import Config
from utils.formatters import html_to_text


def fetch_jobicy_jobs():
    """Fetches job listings from the JobIcy API"""
    try:
        response = requests.get(Config.JOBICY_API_URL, timeout=10)
        response.raise_for_status()
        jobs_data = response.json()
        return jobs_data.get('jobs', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JobIcy jobs data: {e}")
        return []


# print(type(fetch_jobicy_jobs()))
# print(fetch_jobicy_jobs())

def parse_jobicy_job():
    """Parse data from JobIcy API into standardized job format"""
    jobs = fetch_jobicy_jobs()  # Jobs is a list of job dicts
    if not jobs:
        return []
    parsed_jobs = []

    for job in jobs:
        new_job = {}
        new_job["job_title"] = job.get('jobTitle', None)
        new_job["job_url"] = job.get('url', None)
        new_job["company_name"] = job.get('companyName', None)
        job_description = job.get("jobDescription", None)
        if job_description:
            new_job["job_description"] = html_to_text(job_description)
        else:
            new_job["job_description"] = job.get('jobDescription', None)
        new_job["location"] = job.get('jobGeo', None)
        new_job["date_posted"] = job.get('pubDate', None)
        new_job["is_remote"] = None
        new_job["tags"] = job.get('jobIndustry', [])
        parsed_jobs.append(new_job)

    return parsed_jobs
