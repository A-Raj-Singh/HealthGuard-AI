from datetime import date, time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database.database as db_module
from database import models  # noqa: F401
from database.crud import (
    add_health_goal,
    add_medication,
    add_metric,
    add_nutrition,
    authenticate,
    create_patient,
    create_user,
    deactivate_health_goal,
    delete_medication,
    dose_status,
    list_health_goals,
    list_medications,
    list_metrics,
    list_nutrition,
    mark_dose,
)
from database.database import Base


def setup_test_db(tmp_path, monkeypatch):
    """Create an isolated SQLite database for each test."""
    engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}",
        connect_args={"check_same_thread": False},
    )

    Session = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=engine)
    monkeypatch.setattr(db_module, "SessionLocal", Session)


def test_create_patient_and_user(tmp_path, monkeypatch):
    """Test patient creation, user creation, and authentication."""
    setup_test_db(tmp_path, monkeypatch)

    patient = create_patient("Test User", 30, "Other")
    user = create_user(
        "test_unique_user",
        "Password123!",
        "patient",
        patient.id,
    )

    assert patient.id is not None
    assert user is not None

    logged = authenticate(
        "test_unique_user",
        "Password123!",
    )

    assert logged is not None
    assert logged["patient_id"] == patient.id


def test_authentication_and_wrong_password(tmp_path, monkeypatch):
    """Test successful authentication and rejection of an incorrect password."""
    setup_test_db(tmp_path, monkeypatch)

    patient = create_patient("Auth User", 30, "Other")

    create_user(
        "AuthUser",
        "Password123!",
        "patient",
        patient.id,
    )

    # Username is normalized to lowercase.
    logged = authenticate(
        "authuser",
        "Password123!",
    )

    assert logged is not None
    assert logged["username"] == "authuser"
    assert logged["patient_id"] == patient.id

    # Incorrect password must fail.
    failed_login = authenticate(
        "authuser",
        "WrongPassword!",
    )

    assert failed_login is None


def test_duplicate_username_is_rejected(tmp_path, monkeypatch):
    """Test that duplicate usernames cannot be registered."""
    setup_test_db(tmp_path, monkeypatch)

    patient1 = create_patient("First User", 30, "Other")
    patient2 = create_patient("Second User", 31, "Other")

    first_user = create_user(
        "duplicate_user",
        "Password123!",
        "patient",
        patient1.id,
    )

    second_user = create_user(
        "DUPLICATE_USER",
        "AnotherPassword123!",
        "patient",
        patient2.id,
    )

    assert first_user is not None
    assert second_user is None

    # Original account should still work.
    logged = authenticate(
        "duplicate_user",
        "Password123!",
    )

    assert logged is not None
    assert logged["patient_id"] == patient1.id


def test_medication_and_dose_tracking(tmp_path, monkeypatch):
    """Test medication creation, dose tracking, and deactivation."""
    setup_test_db(tmp_path, monkeypatch)

    patient = create_patient(
        "Medication User",
        30,
        "Other",
    )

    medication = add_medication(
        patient.id,
        "Test Medicine",
        "500 mg",
        time(9, 0),
    )

    assert medication.id is not None

    medications = list_medications(patient.id)

    assert len(medications) == 1
    assert medications[0].medicine_name == "Test Medicine"
    assert medications[0].dosage == "500 mg"

    dose_date = date(2026, 9, 11)

    # Dose should initially be pending.
    assert dose_status(
        medication.id,
        patient.id,
        dose_date,
    ) == "pending"

    # Mark dose as taken.
    marked = mark_dose(
        medication.id,
        patient.id,
        dose_date,
    )

    assert marked is True

    assert dose_status(
        medication.id,
        patient.id,
        dose_date,
    ) == "taken"

    # Deactivate medication.
    deleted = delete_medication(
        medication.id,
        patient.id,
    )

    assert deleted is True

    active_medications = list_medications(
        patient.id,
        active_only=True,
    )

    assert len(active_medications) == 0


def test_health_metrics_and_nutrition(tmp_path, monkeypatch):
    """Test health metric and nutrition record creation and retrieval."""
    setup_test_db(tmp_path, monkeypatch)

    patient = create_patient(
        "Health User",
        30,
        "Other",
    )

    metric_date = date(2026, 9, 11)

    metric = add_metric(
        patient.id,
        metric_date,
        steps=6500,
        calories_burned=450,
        sleep_hours=7.5,
        heart_rate=72,
    )

    assert metric.id is not None

    metrics = list_metrics(patient.id)

    assert len(metrics) == 1
    assert metrics[0].steps == 6500
    assert metrics[0].calories_burned == 450
    assert metrics[0].sleep_hours == 7.5
    assert metrics[0].heart_rate == 72

    nutrition = add_nutrition(
        patient.id,
        "Oatmeal",
        calories=300,
        protein_g=10,
        carbs_g=45,
        fat_g=8,
        source="manual",
        log_date=metric_date,
    )

    assert nutrition.id is not None

    nutrition_logs = list_nutrition(
        patient.id,
        log_date=metric_date,
    )

    assert len(nutrition_logs) == 1
    assert nutrition_logs[0].food_name == "Oatmeal"
    assert nutrition_logs[0].calories == 300
    assert nutrition_logs[0].protein_g == 10
    assert nutrition_logs[0].carbs_g == 45
    assert nutrition_logs[0].fat_g == 8


def test_health_goals_and_deactivation(tmp_path, monkeypatch):
    """Test health goal creation, listing, and deactivation."""
    setup_test_db(tmp_path, monkeypatch)

    patient = create_patient(
        "Goal User",
        30,
        "Other",
    )

    goal = add_health_goal(
        patient.id,
        "Daily Steps",
        5000,
        "steps",
    )

    assert goal.id is not None
    assert goal.active is True
    assert goal.goal_type == "Daily Steps"
    assert goal.target_value == 5000
    assert goal.unit == "steps"

    active_goals = list_health_goals(
        patient.id,
        active_only=True,
    )

    assert len(active_goals) == 1
    assert active_goals[0].id == goal.id

    # Deactivate the goal.
    deactivated = deactivate_health_goal(
        goal.id,
        patient.id,
    )

    assert deactivated is True

    # It should no longer appear among active goals.
    active_goals_after = list_health_goals(
        patient.id,
        active_only=True,
    )

    assert len(active_goals_after) == 0

    # It should still exist when requesting all goals.
    all_goals = list_health_goals(
        patient.id,
        active_only=False,
    )

    assert len(all_goals) == 1
    assert all_goals[0].id == goal.id
    assert all_goals[0].active is False