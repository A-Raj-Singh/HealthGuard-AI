from langchain.tools import tool
from database.crud import get_patient, list_medications, list_metrics

@tool
def get_patient_summary(patient_id: int) -> str:
    """Get the stored profile for a patient by patient ID."""
    p = get_patient(patient_id)
    if not p: return 'Patient not found.'
    return f'Patient {p.id}: {p.name}, age {p.age}, gender {p.gender}, height {p.height_cm} cm, weight {p.weight_kg} kg.'

@tool
def get_medications(patient_id: int) -> str:
    """Get the active medication schedule for a patient by patient ID."""
    meds = list_medications(patient_id, active_only=True)
    if not meds: return 'No active medications recorded.'
    return '\n'.join(f'- {m.medicine_name}: {m.dosage} at {m.reminder_time.strftime("%H:%M")}' for m in meds)

@tool
def get_health_metrics(patient_id: int) -> str:
    """Get stored health metrics for a patient by patient ID."""
    metrics = list_metrics(patient_id)
    if not metrics: return 'No health metrics recorded.'
    return '\n'.join(f'- {m.metric_date}: steps={m.steps}, calories_burned={m.calories_burned}, sleep={m.sleep_hours}h, heart_rate={m.heart_rate}' for m in metrics[-10:])
