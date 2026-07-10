#!/usr/bin/env python
"""Stores prompt templates for AI agents"""
import textwrap
from typing import Dict


class Prompts:
    """Class to store prompt templates for AI agents"""
    GENERATION_INSTRUCTIONS = textwrap.dedent("""
        You are a job search assistant that helps job seekers stand out in a competitive market by recommending portfolio projects tailored to specific job openings.
        Analyze the provided job description and recommend **exactly three** portfolio projects that would impress hiring managers for that role.

        Guidelines:
        
        * Recommend projects that solve real-world problems relevant to the role.
        * Ensure each project demonstrates the key skills and technologies mentioned or strongly implied by the job description.
        * Make every recommendation specific, practical, and actionable rather than a generic template.
        * For non-technical roles, recommend projects that demonstrate relevant domain knowledge and transferable skills.
        * For technical roles, recommend projects that showcase current industry-relevant skills and engineering practices.
        * At least one project should be especially memorable by being unusually creative, unconventional, or making effective use of AI or automation where appropriate.
        * Focus on quality and relevance rather than novelty for its own sake.
    """)

    RECOMMENDATION_OUTPUT_SCHEMA = {
    "type": "array",
    "minItems": 3,
    "maxItems": 3,
    "items": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Specific descriptive project title."
            },
            "description": {
                "type": "string",
                "description": "Explain what to build, why it matters, and why it is relevant."
            },
            "technologies": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Technologies, frameworks, languages or tools used."
            },
            "demonstrates": {
                "type": "string",
                "description": "Skills and competencies demonstrated by the project."
            },
            "timeline": {
                "type": "string",
                "description": "Estimated realistic completion time."
            },
            "standout_factor": {
                "type": "string",
                "description": "Why this project would impress hiring managers."
            }
        },
        "required": [
            "title",
            "description",
            "technologies",
            "demonstrates",
            "timeline",
            "standout_factor"
        ],
        "additionalProperties": False
    }
}



    @staticmethod
    def generate_recommendation_prompt(job_data: Dict):
        """Prompt template for generating portfolio project recommendations based on job data"""
        job_description = job_data.get("job_description", "")
        if len(job_description) > 5000:
            job_description = job_description[:5000] + "..."
        prompt = textwrap.dedent(f"""
        Job Title: {job_data.get("job_title", "N/A")}
        Company: {job_data.get("company_name", "N/A")}
        Description: {job_description}
""")
        return prompt

    def extract_title_prompt(user_input: str):
        """Prompt template for extracting job title from user input using LLM"""
        prompt = textwrap.dedent(f"""
        Extract a clean job title from this user input: "{user_input}"
        Focus on identifying the core job title either said explicitly or implied, ignoring extraneous words.
        Return ONLY a JSON object in this exact format (no markdown, no extra text):
        {{
        "status": "True" or "False" (depending on whether a valid title was found),
        "job_title": "Extracted job title or None if no job title found"
        
        }}
        
        """)
        return prompt
