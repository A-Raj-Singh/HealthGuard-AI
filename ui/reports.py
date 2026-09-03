import streamlit as st
from services.report_service import report_data, metrics_csv, health_pdf

def render(patient_id):
    st.title('📄 Health Reports')
    patient, metrics, medications, nutrition = report_data(patient_id)
    if not patient: st.error('Patient not found.'); return
    st.write(f'**Patient:** {patient.name}  |  **Age:** {patient.age}')
    csv_bytes = metrics_csv(metrics)
    st.download_button('Download health metrics CSV', csv_bytes, 'health_metrics.csv', 'text/csv')
    pdf_bytes = health_pdf(patient, metrics, medications)
    st.download_button('Download PDF health report', pdf_bytes, 'health_report.pdf', 'application/pdf')
