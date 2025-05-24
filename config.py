# multi_agent_tutor/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("AIzaSyCpTNCC8uGE3ils-9Ad92uDEVQYg1bao4M")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment variables. Please ensure it is set.")

# You can add other configurations here, like model names
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash-latest" # Or "gemini-pro"