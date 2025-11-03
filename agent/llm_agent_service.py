#!/usr/bin/env python
"""LLM Agent Service to handle interactions with the language model"""
import google.generativeai as genai
from config import Config
import os
import json
from typing import Dict, List, Optional

# Configure the Gemini API key
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_recommendations(job_data: Dict) -> Optional[List[Dict]]:
    """Generate portfolio project recommendations based on job data using Gemini LLM"""
    try:
        prompt = build_prompt(job_data)
        response = model.generate_content(prompt)
        recommendations = parse_response(response.text)
        return recommendations
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return None

def build_prompt(job_data: Dict) -> str:
    """Build the prompt for the LLM based on job data"""

    # Truncate job description if too long
    description = job_data.get("job_description", "")
    if len(description) > 1000:
        description = description[:1000] + "..."
    prompt = f"""
        You are an expert career advisor helping job seekers create portfolio projects that align them as top candidates for job roles.
        Analyze this job and recommend 3 top portfolio projects that would impress hiring managers for this role.
        Job Title: {job_data.get("job_title", "N/A")}
        Company: {job_data.get("company_name", "N/A")}
        Description: {description}
        
        Requirements:
        - Provide 3 distinct portfolio project ideas.
        - Each project should be buildable within 2-4 weeks.
        - Projects must demonstrate key skills relevant to the job.
        - Be specific and practical.
        - Return only a JSON object in this exact format (no markdown, no extra text):
        {{
        "projects": [
        {{
        "title": "Specific Project Name,
        "description": "What to build in 2 - 3 sentences.",
        "technologies": ["Tech1", "Tech2", "..."],
        "demonstrates": "Which job skills this prove",
        "timeline": "Estimated time to build"
        }},
      ]
      }}
    Generate exactly 3 projects. Return only JSON, nothing else.      
"""
    return prompt

def parse_response(response_text: str) -> Optional[List[Dict]]:
    """Parse Gemini response to structure data"""
    try:
        # Remove markdown code block if present
        response_text = response_text.strip()
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            response_text = '\n'.join(lines[1:-1]).strip()

        # Parse JSON
        data = json.loads(response_text)

        # Extract projects
        projects = data.get("projects", [])

        # Validate we have 3 projects
        if len(projects) < 1:
            return None
        return projects[:3]

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response was: {response_text:200}")
        return None
    except Exception as e:
        print(f"Parse error: {e}")
        return None

