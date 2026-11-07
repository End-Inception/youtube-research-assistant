
import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gemini-3.8-flash"
)

if not YOUTUBE_API_KEY:
    raise ValueError("Missing YOUTUBE_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY")
