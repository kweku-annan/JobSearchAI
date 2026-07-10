#!/usr/bin/env python
"""Agent Handler"""
from agent.llm_agent_service import generate_recommendations
from utils.intent_detector import extract_job_title
from services.cache_logic import get_cached_jobs_by_title, caching_logic
from utils.formatters import format_job_response, format_no_jobs_message
from utils.prompts import Prompts
from config import settings

from openai import OpenAI


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
    instruction = Prompts.GENERATION_INSTRUCTIONS
    base_url = settings.OPEN_ROUTER_BASE_URL
    api_key = settings.LLM_KEY
    llm_client = OpenAI(api_key=api_key, base_url=base_url)

    print(f"Extracted job title from user message: {job_title}")
    if not job_title:
        return (
            "🤔 I couldn't identify a job title from your message.\n\n"
            "Try something like:\n"
            "• 'python developer'\n"
            "• 'looking for backend engineer jobs'\n"
            "• 'show me data analyst positions'\n\n"
        )

    caching_logic() # Ensure cache is populated and fresh
    cached_jobs = get_cached_jobs_by_title(job_title) # Could have called Db.get_by_title here

    if not cached_jobs:
        return format_no_jobs_message(job_title)


    # Generate recommendations based on the first job
    recommendations = None
    try:
        first_cached_job = cached_jobs[0].to_dict()
        # jobs_formatter_test = format_job_response(cached_jobs, recommendations, job_title)
        recommendations = generate_recommendations(first_cached_job, llm_client=llm_client, instructions=instruction, model="tencent/hy3:free")
    except Exception as e:
        print(f"LLM recommendation error: {e}")

    print(f"Recommendations over here!: {recommendations}")

    # Format and return the job response
    response = format_job_response(cached_jobs, recommendations, job_title)
    return response









