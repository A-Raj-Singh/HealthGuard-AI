import streamlit as st
import pandas as pd
from datetime import date
from services.nutrition_service import analyze_and_save, history
from config import SPOONACULAR_API_KEY

def render(patient_id):
    st.title('🥗 Nutrition Tracker')
    if SPOONACULAR_API_KEY: st.success('Spoonacular nutrition lookup is enabled.')
    else: st.info('No Spoonacular key detected. You can still record nutrition manually.')
    with st.form('nutrition_form'):
        food = st.text_input('Food / meal name')
        a,b,c = st.columns(3)
        calories = a.number_input('Calories', 0.0, step=10.0)
        protein = b.number_input('Protein (g)', 0.0, step=1.0)
        carbs = c.number_input('Carbs (g)', 0.0, step=1.0)
        fat = st.number_input('Fat (g)', 0.0, step=1.0)
        if st.form_submit_button('Analyze & save', type='primary'):
            if food.strip():
                obj = analyze_and_save(patient_id, food.strip(), calories, protein, carbs, fat); st.success(f'Saved using {obj.source}.'); st.rerun()
            else: st.error('Enter a food name.')
    logs = history(patient_id)
    if logs:
        df = pd.DataFrame([{'Date':x.log_date,'Food':x.food_name,'Calories':x.calories,'Protein (g)':x.protein_g,'Carbs (g)':x.carbs_g,'Fat (g)':x.fat_g,'Source':x.source} for x in logs])
        st.subheader('Nutrition history')
        st.dataframe(df, use_container_width=True, hide_index=True)
