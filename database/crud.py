from datetime import date, datetime, time
from sqlalchemy import select
from .database import get_session
from .models import DoseLog, HealthGoal, HealthMetric, Medication, NutritionLog, Patient, User
from auth.password import hash_password, verify_password


def create_patient(name, age, gender, height_cm=None, weight_kg=None):
    with get_session() as db:
        obj = Patient(name=name, age=age, gender=gender, height_cm=height_cm, weight_kg=weight_kg)
        db.add(obj); db.commit(); db.refresh(obj); return obj

def get_patient(patient_id):
    with get_session() as db:
        return db.get(Patient, patient_id)

def list_patients():
    with get_session() as db:
        return list(db.scalars(select(Patient).order_by(Patient.id)))

def create_user(username, password, role='patient', patient_id=None):
    with get_session() as db:
        if db.scalar(select(User).where(User.username == username.lower().strip())):
            return None
        user = User(username=username.lower().strip(), password_hash=hash_password(password), role=role, patient_id=patient_id)
        db.add(user); db.commit(); db.refresh(user); return user

def authenticate(username, password):
    with get_session() as db:
        user = db.scalar(select(User).where(User.username == username.lower().strip()))
        if user and verify_password(password, user.password_hash):
            return {'id': user.id, 'username': user.username, 'role': user.role, 'patient_id': user.patient_id}
        return None

def add_medication(patient_id, medicine_name, dosage, reminder_time):
    with get_session() as db:
        med = Medication(patient_id=patient_id, medicine_name=medicine_name, dosage=dosage, reminder_time=reminder_time)
        db.add(med); db.commit(); db.refresh(med); return med

def list_medications(patient_id, active_only=False):
    with get_session() as db:
        stmt = select(Medication).where(Medication.patient_id == patient_id)
        if active_only: stmt = stmt.where(Medication.active.is_(True))
        return list(db.scalars(stmt.order_by(Medication.reminder_time)))

def delete_medication(medication_id, patient_id):
    with get_session() as db:
        med = db.scalar(select(Medication).where(Medication.id == medication_id, Medication.patient_id == patient_id))
        if not med: return False
        med.active = False; db.commit(); return True

def mark_dose(medication_id, patient_id, dose_date=None):
    dose_date = dose_date or date.today()
    with get_session() as db:
        med = db.scalar(select(Medication).where(Medication.id == medication_id, Medication.patient_id == patient_id))
        if not med: return False
        dose = db.scalar(select(DoseLog).where(DoseLog.medication_id == medication_id, DoseLog.dose_date == dose_date))
        if not dose:
            dose = DoseLog(medication_id=medication_id, patient_id=patient_id, dose_date=dose_date)
            db.add(dose)
        dose.status = 'taken'; dose.taken_at = datetime.now(); db.commit(); return True

def dose_status(medication_id, patient_id, dose_date=None):
    dose_date = dose_date or date.today()
    with get_session() as db:
        dose = db.scalar(
            select(DoseLog).where(
                DoseLog.medication_id == medication_id,
                DoseLog.patient_id == patient_id,
                DoseLog.dose_date == dose_date,
            )
        )
        return dose.status if dose else 'pending'


def dose_statuses(patient_id, dose_date=None):
    dose_date = dose_date or date.today()
    with get_session() as db:
        rows = db.execute(
            select(DoseLog.medication_id, DoseLog.status).where(
                DoseLog.patient_id == patient_id,
                DoseLog.dose_date == dose_date,
            )
        ).all()
        return {medication_id: status for medication_id, status in rows}

def add_metric(patient_id, metric_date, steps, calories_burned, sleep_hours, heart_rate):
    with get_session() as db:
        obj = HealthMetric(patient_id=patient_id, metric_date=metric_date, steps=steps, calories_burned=calories_burned, sleep_hours=sleep_hours, heart_rate=heart_rate)
        db.add(obj); db.commit(); db.refresh(obj); return obj

def list_metrics(patient_id):
    with get_session() as db:
        return list(db.scalars(select(HealthMetric).where(HealthMetric.patient_id == patient_id).order_by(HealthMetric.metric_date)))

def add_nutrition(patient_id, food_name, calories, protein_g, carbs_g, fat_g, source='manual', log_date=None):
    with get_session() as db:
        obj = NutritionLog(patient_id=patient_id, food_name=food_name, calories=calories, protein_g=protein_g, carbs_g=carbs_g, fat_g=fat_g, source=source, log_date=log_date or date.today())
        db.add(obj); db.commit(); db.refresh(obj); return obj

def list_nutrition(patient_id, log_date=None):
    with get_session() as db:
        stmt = select(NutritionLog).where(NutritionLog.patient_id == patient_id)
        if log_date: stmt = stmt.where(NutritionLog.log_date == log_date)
        return list(db.scalars(stmt.order_by(NutritionLog.log_date.desc(), NutritionLog.id.desc())))

def add_health_goal(patient_id, goal_type, target_value, unit):
    with get_session() as db:
        goal = HealthGoal(
            patient_id=patient_id,
            goal_type=goal_type,
            target_value=target_value,
            unit=unit,
            active=True,
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        return goal


def list_health_goals(patient_id, active_only=True):
    with get_session() as db:
        stmt = select(HealthGoal).where(
            HealthGoal.patient_id == patient_id
        )

        if active_only:
            stmt = stmt.where(HealthGoal.active.is_(True))

        return list(
            db.scalars(
                stmt.order_by(HealthGoal.id.desc())
            )
        )


def deactivate_health_goal(goal_id, patient_id):
    with get_session() as db:
        goal = db.scalar(
            select(HealthGoal).where(
                HealthGoal.id == goal_id,
                HealthGoal.patient_id == patient_id,
            )
        )

        if not goal:
            return False

        goal.active = False
        db.commit()
        return True
