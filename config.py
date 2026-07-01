#!/usr/bin/env python
"""Configuration settings for the application"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    # Application
    LLM_KEY: str
    ARBEITNOW_API_URL: str
    JOBICY_API_URL: str
    REMOTEOK_API_URL: str
    REMOTIVE_API_URL: str
    OPEN_ROUTER_BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=True,
    )


    # class Config:
    #     env_file = ".env"
    #     case_sensitive = True


settings = Settings()



# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# class Config:
#     """Base configuration class"""
#     OPENAI_API_KEY = os.getenv("LLM_KEY")
#
#     # API URLs
#     ARBEITNOW_API_URL = "https://www.arbeitnow.com/api/job-board-api" # Last resort
#     JOBICY_API_URL = "https://www.jobicy.com/api/v2/remote-jobs" # 3rd resort
#     REMOTEOK_API_URL = "https://remoteok.com/api" # 2nd resort
#     REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs" # 1st resort
