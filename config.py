# multi_agent_tutor/config.py
import os
from dotenv import load_dotenv

load_dotenv() # This is fine to keep, it won't find a .env on Railway but doesn't hurt

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment variables. Please ensure it is set.")

DEFAULT_GEMINI_MODEL = "gemini-1.5-flash-latest"