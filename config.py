#!/usr/bin/env python
"""Configuration settings for the application"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    OPENAI_API_KEY = os.getenv("OPENAI_KEY")

    # API URLs
    ARBEITNOW_API_URL = "https://www.arbeitnow.com/api/job-board-api" # Last resort
    JOBICY_API_URL = "https://www.jobicy.com/api/v2/remote-jobs" # 3rd resort
    REMOTEOK_API_URL = "https://remoteok.com/api" # 2nd resort
    REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs" # 1st resort
