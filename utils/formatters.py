#!/usr/bin/env python
"""Parse texts"""

from bs4 import BeautifulSoup
from typing import Optional, List, Dict


def html_to_text(html_content):
    """Convert HTML content to plain text"""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text().strip()

def format_job_response(jobs: Dict, recommendations: Optional[List[Dict]], job_title:str) -> str:
    """
    Format jobs and recommendations into a nice message

    :param jobs: List of jobs object from database
    :param recommendations: List of recommendation dicts or None
    :param job_title:
    :return: The search term user used
    """

    if not jobs:
        return format_no_jobs_message(job_title)

    # Start building the message
    message = f"Found {len(jobs)} {job_title} position{'s' if len(jobs) > 1 else ''}!:\n\n"

    # Add recommendations if available
    if recommendations:
        first_job = jobs
        message += f"Portfolio Project Recommendations\n"
        message += f"_(Based on: {first_job['job_title']} at {first_job['company_name']})_\n\n"

        for i, rec in enumerate(recommendations, 1):
            message += f"{i}.  {rec['title']}\n"
            message += f"   • {rec['description']}\n"
            message += f"   • Stack: {', '.join(rec['technologies'])}\n"
            message += f"   • Demonstrates: {rec['demonstrates']}\n"
            message += f"   • Time: {rec['timeline']}\n\n"

    else:
        message += "No portfolio project recommendations available at this time. Try something else\n\n"

        # # Add all jobs
        # message += "📋 **Available Positions:**\n\n"
        #
        # for i, job in enumerate(jobs, 1):
        #     message += f"{i}. **{job['job_title']}** @ {job['company_name']}\n"
        #     desc = job['description'][:150] + "..." if len(job['description']) > 150 else job['description']
        #     message += f"{desc}\n"
        #
        #     if job['url']:
        #         message += f"   🔗 [Apply Here]({job['url']})\n"
        #
        #     message += "\n"

    return message


def format_no_jobs_message(job_title: str) -> str:
    """Message when no jobs found in the database"""
    return f"""No cached jobs found for "{job_title}". Please try again later or "Try something like:\n"
            "• 'python developer'\n"
            "• 'looking for backend engineer jobs'\n"
            "• 'show me data analyst positions'\n\n."""
