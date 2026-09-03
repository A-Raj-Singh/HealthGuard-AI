import requests
from config import SPOONACULAR_API_KEY

URL = 'https://api.spoonacular.com/recipes/guessNutrition'

def guess_nutrition(food: str):
    if not SPOONACULAR_API_KEY or not food.strip():
        return None
    try:
        r = requests.get(URL, params={'title': food, 'apiKey': SPOONACULAR_API_KEY}, timeout=10)
        r.raise_for_status(); data = r.json()
        return {
            'calories': float(data.get('calories', {}).get('value', 0)),
            'protein_g': float(data.get('protein', {}).get('value', 0)),
            'carbs_g': float(data.get('carbs', {}).get('value', 0)),
            'fat_g': float(data.get('fat', {}).get('value', 0)),
            'source': 'Spoonacular'
        }
    except (requests.RequestException, ValueError, TypeError):
        return None
