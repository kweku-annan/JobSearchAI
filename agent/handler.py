#!/usr/bin/env python
"""Agent Handler"""
from agent.llm_agent_service import generate_recommendations
# In agent/handler.py
from utils.intent_detector import extract_job_title
from services.cache_logic import get_cached_jobs_by_title, caching_logic
from utils.formatters import format_job_response, format_no_jobs_message


def process_message(user_message):
    """Main entry point to process user messages"""
    try:
        return handle_job_search(user_message)
    except Exception as e:
        print(f"Error processing message: {e}")
        return "😞 Sorry, something went wrong while processing your request."



def handle_job_search(message: str) -> str:
    """Handle job search requests from users."""

    # Extract job title from user message
    job_title = extract_job_title(message)
    if not job_title:
        return (
            "🤔 I couldn't identify a job title from your message.\n\n"
            "Try something like:\n"
            "• 'python developer'\n"
            "• 'looking for backend engineer jobs'\n"
            "• 'show me data analyst positions'\n\n"
        )

    caching_logic() # Ensure cache is populated and fresh
    cached_jobs = get_cached_jobs_by_title(job_title)

    if not cached_jobs:
        return format_no_jobs_message(job_title)

    # Generate recommendations based on the first job
    recommendations = None
    try:
        cached_jobs = [jobs.to_dict() for jobs in cached_jobs]
        recommendations = generate_recommendations(cached_jobs[0])
    except Exception as e:
        print(f"LLM recommendation error: {e}")

    # Format and return the job response
    response = format_job_response(cached_jobs, recommendations, job_title)
    return response









