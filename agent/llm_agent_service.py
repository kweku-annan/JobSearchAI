#!/usr/bin/env python
"""LLM Agent Service to handle interactions with the language model"""
from utils.prompts import Prompts
from pprint import pprint
from openai import OpenAI
from config import Config
import json
from typing import Dict, List, Optional

# OpenAI client will be initialized when needed
_client = None

def get_client():
    """Get or initialize the OpenAI client"""
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

        )
    return _client

def generate_recommendations(job_data: Dict) -> Optional[List[Dict]]:
    """Generate portfolio project recommendations based on job data using OpenAI LLM"""
    try:
        client = get_client()
        prompt = Prompts.generate_recommendation_prompt(job_data)
        response = client.responses.create(
            model="gemini-2.5-flash",
            input=[
                {"role": "system", "content": "You are an expert career advisor helping job seekers create portfolio projects that align them as top candidates for job roles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            # response_format={"type": "json_object"}
        )
        recommendations = parse_response(response.choices[0].message.content)
        # pprint(recommendations)
        return recommendations
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return None

def parse_response(response_text: str) -> Optional[List[Dict]]:
    """Parse OpenAI response to structure data"""
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
        # print("==================PROJECTS==================")
        # pprint(projects[:3])
        return projects[:3]

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response was: {response_text:200}")
        return None
    except Exception as e:
        print(f"Parse error: {e}")
        return None

