#!/usr/bin/env python
"""LLM Agent Service to handle interactions with the language model"""
from utils.prompts import Prompts
from pprint import pprint
import google.generativeai as genai
from config import Config
import json
from typing import Dict, List, Optional

# Configure the Gemini API key
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_recommendations(job_data: Dict) -> Optional[List[Dict]]:
    """Generate portfolio project recommendations based on job data using Gemini LLM"""
    try:
        prompt = Prompts.generate_recommendation_prompt(job_data)
        response = model.generate_content(prompt)
        recommendations = parse_response(response.text)
        # pprint(recommendations)
        return recommendations
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return None

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

