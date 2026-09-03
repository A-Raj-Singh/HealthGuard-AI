import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database.crud import get_patient, list_metrics, add_metric
from services.analytics import adherence_percentage, nutrition_totals

def render(patient_id):
    patient = get_patient(patient_id)
    if not patient:
        st.error('Patient record not found.'); return
    st.title(f'Welcome, {patient.name} 👋')
    st.caption('Your personal health overview')
    metrics = list_metrics(patient_id)
    totals = nutrition_totals(patient_id)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric('Medication adherence', f'{adherence_percentage(patient_id)}%')
    c2.metric('Calories today', f"{totals['calories']:.0f}")
    c3.metric('Protein today', f"{totals['protein_g']:.1f} g")
    c4.metric('Health entries', len(metrics))
    st.subheader('Add daily health metrics')
    with st.form('metrics_form'):
        a,b,c,d = st.columns(4)
        metric_date = a.date_input('Date', value=date.today())
        steps = b.number_input('Steps', min_value=0, step=100)
        calories = c.number_input('Calories burned', min_value=0.0, step=10.0)
        sleep = d.number_input('Sleep hours', min_value=0.0, max_value=24.0, step=0.5)
        heart = st.number_input('Heart rate (bpm)', min_value=0, max_value=250, value=70)
        if st.form_submit_button('Save health metrics', type='primary'):
            add_metric(patient_id, metric_date, int(steps), float(calories), float(sleep), int(heart)); st.success('Saved.'); st.rerun()
    if metrics:
        df = pd.DataFrame([{'Date':m.metric_date,'Steps':m.steps,'Sleep':m.sleep_hours,'Heart Rate':m.heart_rate} for m in metrics])
        st.subheader('Progress')
        st.plotly_chart(px.line(df, x='Date', y='Steps', markers=True, title='Steps over time'), use_container_width=True)
        st.plotly_chart(px.line(df, x='Date', y='Sleep', markers=True, title='Sleep over time'), use_container_width=True)
