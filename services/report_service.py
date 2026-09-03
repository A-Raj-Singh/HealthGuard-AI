import io
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from database.crud import get_patient, list_metrics, list_medications, list_nutrition

def report_data(patient_id):
    return get_patient(patient_id), list_metrics(patient_id), list_medications(patient_id), list_nutrition(patient_id)

def metrics_csv(metrics):
    df = pd.DataFrame([{'Date':m.metric_date,'Steps':m.steps,'Calories Burned':m.calories_burned,'Sleep Hours':m.sleep_hours,'Heart Rate':m.heart_rate} for m in metrics])
    return df.to_csv(index=False).encode('utf-8')

def health_pdf(patient, metrics, medications):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet(); story = [Paragraph('HealthGuard AI - Health Report', styles['Title']), Spacer(1, 10)]
    story.append(Paragraph(f'Patient: {patient.name} | Age: {patient.age} | Gender: {patient.gender}', styles['BodyText']))
    story.append(Spacer(1, 10))
    story.append(Paragraph('Medications', styles['Heading2']))
    med_rows = [['Medicine','Dosage','Reminder']] + [[m.medicine_name,m.dosage,m.reminder_time.strftime('%H:%M')] for m in medications]
    story.append(Table(med_rows, repeatRows=1, style=TableStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey)])))
    story.append(Spacer(1, 12)); story.append(Paragraph('Health Metrics', styles['Heading2']))
    metric_rows = [['Date','Steps','Calories','Sleep','Heart Rate']] + [[str(m.metric_date),m.steps,m.calories_burned,m.sleep_hours,m.heart_rate] for m in metrics]
    story.append(Table(metric_rows, repeatRows=1, style=TableStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey)])))
    doc.build(story); return buffer.getvalue()
