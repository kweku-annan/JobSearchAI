#!/usr/bin/env python
"""Parse texts"""
from pprint import pprint
from bs4 import BeautifulSoup
from typing import Optional, List, Dict


def html_to_text(html_content):
    """Convert HTML content to plain text"""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text().strip()

def format_job_response(jobs: List, recommendations: Optional[List[Dict]], job_title:str) -> str:
    """
    Format jobs and recommendations into a nice message

    :param jobs: List of jobs object from database
    :param recommendations: List of recommendation dicts or None
    :param job_title:
    :return: The search term user used

    ===========JOBS FOUND===========
    Example: Here is a list of jobs for {job_title}:
    1. Job Title @ Company Name - [Apply Here](url)
       Description: Short description...
    2. Job Title @ Company Name - [Apply Here](url)
       Description: Short description...
    3. ...

    ==========PORTFOLIO RECOMMENDATIONS===========
    Based on: {first_job_title} at {first_company_name}..
    Portfolio Project Recommendations:
    """

    if not jobs:
        return format_no_jobs_message(job_title)

    # Start building the message
    # print("==================JOBS FOUND==================")
    # pprint(jobs)
    message = f"Here is a list of jobs for '{job_title.title()}':\n\n"
    all_jobs_list = [jobs.to_dict() for jobs in jobs]

    # Add all jobs to message
    for i, job in enumerate(all_jobs_list, 1):
        message += f"{i}. {job['job_title'].title()} @ {job['company_name']} - {job['location']} - "
        if job.get('job_url'):
            message += f"[Apply Here]({job['job_url']})\n"
        else:
            message += "\n"

        # Add description (truncate if too long)
        desc = job.get('job_description', 'No description available')
        if len(desc) > 150:
            desc = desc[:150] + "..."
        message += f"   Description: {desc}\n\n"

    # Add recommendations if available
    if recommendations:
        first_job = jobs[0].to_dict()  # Assuming jobs are objects with a to_dict method
        message += f"Portfolio Project Recommendations\n"
        message += f"Based on: {first_job['job_title']} at {first_job['company_name']}\n"

        for i, rec in enumerate(recommendations, 1):
            message += f"{i}.  {rec['title']}\n"
            message += f"   • {rec['description']}\n"
            message += f"   • Stack: {', '.join(rec['technologies'])}\n"
            message += f"   • Demonstrates: {rec['demonstrates']}\n"
            message += f"   • Time: {rec['timeline']}\n\n"

    else:
        message += "No portfolio project recommendations available at this time.\n"


    return message


def format_no_jobs_message(job_title: str) -> str:
    """Message when no jobs found in the database"""
    return f"""No cached jobs found for "{job_title}". Please try again later or "Try something like:\n"
            "--'python developer'\n"
            "--'looking for backend engineer jobs'\n"
            "--'show me data analyst positions'\n\n."""
