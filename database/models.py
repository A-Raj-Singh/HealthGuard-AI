from datetime import date, datetime, time
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(30), default='patient')
    patient_id: Mapped[int | None] = mapped_column(ForeignKey('patients.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    patient: Mapped['Patient | None'] = relationship(back_populates='user')

class Patient(Base):
    __tablename__ = 'patients'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(30), default='Prefer not to say')
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped['User | None'] = relationship(back_populates='patient', uselist=False)
    medications: Mapped[list['Medication']] = relationship(back_populates='patient', cascade='all, delete-orphan')
    doses: Mapped[list['DoseLog']] = relationship(back_populates='patient', cascade='all, delete-orphan')
    metrics: Mapped[list['HealthMetric']] = relationship(back_populates='patient', cascade='all, delete-orphan')
    nutrition_logs: Mapped[list['NutritionLog']] = relationship(back_populates='patient', cascade='all, delete-orphan')
     health_goals: Mapped[list['HealthGoal']] = relationship(
        back_populates='patient',
        cascade='all, delete-orphan'
    )

class Medication(Base):
    __tablename__ = 'medications'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'), index=True)
    medicine_name: Mapped[str] = mapped_column(String(120))
    dosage: Mapped[str] = mapped_column(String(80))
    reminder_time: Mapped[time] = mapped_column(Time)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    patient: Mapped['Patient'] = relationship(back_populates='medications')
    dose_logs: Mapped[list['DoseLog']] = relationship(back_populates='medication', cascade='all, delete-orphan')

class DoseLog(Base):
    __tablename__ = 'dose_logs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    medication_id: Mapped[int] = mapped_column(ForeignKey('medications.id'), index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'), index=True)
    dose_date: Mapped[date] = mapped_column(Date, default=date.today, index=True)
    taken_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default='pending')
    medication: Mapped['Medication'] = relationship(back_populates='dose_logs')
    patient: Mapped['Patient'] = relationship(back_populates='doses')

class HealthMetric(Base):
    __tablename__ = 'health_metrics'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'), index=True)
    metric_date: Mapped[date] = mapped_column(Date, default=date.today, index=True)
    steps: Mapped[int] = mapped_column(Integer, default=0)
    calories_burned: Mapped[float] = mapped_column(Float, default=0)
    sleep_hours: Mapped[float] = mapped_column(Float, default=0)
    heart_rate: Mapped[int] = mapped_column(Integer, default=0)
    patient: Mapped['Patient'] = relationship(back_populates='metrics')

class NutritionLog(Base):
    __tablename__ = 'nutrition_logs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'), index=True)
    food_name: Mapped[str] = mapped_column(String(160))
    calories: Mapped[float] = mapped_column(Float, default=0)
    protein_g: Mapped[float] = mapped_column(Float, default=0)
    carbs_g: Mapped[float] = mapped_column(Float, default=0)
    fat_g: Mapped[float] = mapped_column(Float, default=0)

class HealthGoal(Base):
    __tablename__ = 'health_goals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey('patients.id'),
        index=True
    )

    goal_type: Mapped[str] = mapped_column(String(50))
    target_value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(30))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    patient: Mapped['Patient'] = relationship(
        back_populates='health_goals'
    )
