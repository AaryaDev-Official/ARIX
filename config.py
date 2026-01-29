import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    USER_NAME = os.getenv("USER_NAME", "User")
    BOT_NAME = os.getenv("ASSISTANT_NAME", "ARIX")
    CITY = os.getenv("CITY", "London")