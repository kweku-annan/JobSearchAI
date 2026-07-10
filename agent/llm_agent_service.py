#!/usr/bin/env python
"""LLM Agent Service to handle interactions with the language model"""
from openai import OpenAI
import json
from typing import Dict, List, Optional

from utils.prompts import Prompts

def generate_recommendations(
        job_data: Dict, llm_client: OpenAI, instructions: str, model: str = "openai/gpt-oss-120b"
) -> Optional[List[Dict]]:
    """
    Generate portfolio recommendations for a job using LLM.
    :param job_data: Dictionary containing job information.
    :param llm_client: The LLM client responsible for generating recommendations.
    :param instructions: System instructions for the LLM.
    :param model: llm model to use
    :return: A list of jobs recommendations.
    """
    try:
        job_data = Prompts.generate_recommendation_prompt(job_data)
        output_schema = Prompts.RECOMMENDATION_OUTPUT_SCHEMA
        message = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": job_data},
        ]

        response = llm_client.responses.create(
            model=model,
            input=message,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "portfolio_project_recommendations",
                    "schema": output_schema,
                    "strict": True,
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


