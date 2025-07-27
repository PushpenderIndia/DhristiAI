"""
Configuration file for DrishtiAI Multi-Agent System
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys and Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() == "true"
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# Model Configuration  
# Using gemini-1.5-flash for higher rate limits on free tier
DEFAULT_MODEL = "gemini-1.5-flash"
BACKUP_MODEL = "gemini-1.5-flash"

# Agent Configuration
MAX_RETRY_ATTEMPTS = 3
TIMEOUT_SECONDS = 30
DEFAULT_TEMPERATURE = 0.3  # Lower temperature for more focused responses
MAX_OUTPUT_TOKENS = 1000   # Limit output to reduce quota usage
REQUEST_DELAY_SECONDS = 2  # Delay between requests to avoid rate limits

# Stampede Risk Thresholds
RISK_THRESHOLDS = {
    "LOW": 0.3,
    "MEDIUM": 0.6,
    "HIGH": 0.8,
    "CRITICAL": 0.9
}

# Social Media APIs (add your keys)
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
REDDIT_API_KEY = os.getenv("REDDIT_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Weather API
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Traffic and Maps API
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def validate_config():
    """Validate that required configuration is present"""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    return True 