from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    OPENAI_KEY = os.getenv('OPENAI_KEY')
    POSTGRE_URL = os.getenv('POSTGRE_URL')
    NEO4J_URL = os.getenv('NEO4J_URL')
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
    HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')

