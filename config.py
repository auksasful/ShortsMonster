from dotenv import load_dotenv
import os

load_dotenv()  # Loading environment variables from the .env file

class Config:
    # API keys
    NAGA_AC_API_KEY = os.getenv("NAGA_AC_API_KEY")
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

    # Video parameters
    VIDEO_WIDTH = 1080
    VIDEO_HEIGHT = 1920