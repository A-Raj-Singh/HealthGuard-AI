import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / '.env')

DATA_DIR = ROOT_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)
DATABASE_URL = os.getenv('DATABASE_URL', f"sqlite:///{DATA_DIR / 'healthcare.db'}")

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY', '')

APP_NAME = 'HealthGuard AI'
MEDICAL_DISCLAIMER = (
    'Educational information only. This application does not diagnose, treat, '
    'or replace advice from a qualified healthcare professional.'
)
