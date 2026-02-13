#!/usr/bin/env python
"""Stores prompt templates for AI agents"""
import textwrap
from typing import Dict


class Prompts:
    """Class to store prompt templates for AI agents"""

    @staticmethod
    def generate_recommendation_prompt(job_data: Dict):
        """Prompt template for generating portfolio project recommendations based on job data"""
        job_description = job_data.get("job_description", "")
        if len(job_description) > 5000:
            job_description = job_description[:5000] + "..."
        prompt = textwrap.dedent(f"""
        You are an expert career advisor helping job seekers create portfolio projects that align them as top candidates for job roles.
        Analyze this job and recommend 3 top portfolio projects that would impress hiring managers for this role.
        Job Title: {job_data.get("job_title", "N/A")}
        Company: {job_data.get("company_name", "N/A")}
        Description: {job_description}
        
        Requirements:
        - Provide 3 distinct portfolio project ideas that solve real-world problems relevant to this role.
        - Projects should demonstrate key skills and technologies mentioned in or implied by the job description.
        - Make projects specific and actionable, not generic templates.
        - If job is a non-technical role, recommend projects that demonstrate relevant soft skills and domain knowledge.
        - If job is a technical, role, recommend projects that demonstrate 2026 high-demand relevant skills for that role. 
        - One of the projects must satisfy at least one of the following criteria:
                - Must be creative or unconventional and stands out from typical projects
                - Sound stupid but impressive
                - If relevant to the role, consider how AI/automation tools could enhance it.
        - Be specific and practical.
        - Return ONLY a JSON object in this exact format (no markdown, no extra text):
        {{
        "projects": [
        {{
        "title": "Specific descriptive project name",
        "description": "Clear 2 - 5 sentence explanation of what to build and why it's relevant to the job    ",
        "technologies": ["Tech1", "Tech2", "..."],
        "demonstrates": "Specific skills from the job description this project proves",
        "timeline": "Realistic estimated completion time (e.g. '1 week', '2 months') based on the scope of the project",
        "standout_factor": "Why this project would impress hiring managers."
        }}
        ]
        }}
    Ensure the JSON is complete and properly formatted.
""")
        return prompt
