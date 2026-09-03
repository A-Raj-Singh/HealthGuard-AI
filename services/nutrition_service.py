from api.nutrition_api import guess_nutrition
from database.crud import add_nutrition, list_nutrition

def analyze_and_save(patient_id, food, calories, protein_g, carbs_g, fat_g):
    api_data = guess_nutrition(food)
    if api_data:
        return add_nutrition(patient_id, food, **api_data)
    return add_nutrition(patient_id, food, calories, protein_g, carbs_g, fat_g, source='manual')

def history(patient_id):
    return list_nutrition(patient_id)
