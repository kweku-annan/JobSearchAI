#!/usr/bin/env python
"""LLM Agent Service to handle interactions with the language model"""
from utils.prompts import Prompts
from pprint import pprint
from openai import OpenAI
from config import settings
import json
from typing import Dict, List, Optional

# OpenAI client will be initialized when needed

def generate_recommendations(
        job_data: Optional[List[Dict]], llm_client: OpenAI, instructions: str, model: str = "openai/gpt-oss-120b"
) -> Optional[List[Dict]]:
    """
    Generate portfolio recommendations for a job using LLM.
    :param job_data: List of job data (dictionaries).
    :param llm_client: The LLM client responsible for generating recommendations.
    :param instructions: System instructions for the LLM.
    :param model: llm model to use
    :return: A list of jobs recommendations.
    """
    try:
        message = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": job_data},
        ]

        response = llm_client.responses.create(
            model=model,
            input=message,
            text={
                "format": {
                    "type": "json_object"
                }
            }
        )
        recommendations = response.output_text
        return json.loads(recommendations)
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": str(type(e).__name__),
                "message": str(e)
            }
        }


def parse_response(response_text: str) -> Optional[List[Dict]]:
    """Parse OpenAI response to structured data"""
    try:
        # Remove markdown code block if present
        response_text = response_text.strip()
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            response_text = '\n'.join(lines[1:-1]).strip()

        # Parse JSON
        data = json.loads(response_text)

        if data.get("status"):
            return data

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

