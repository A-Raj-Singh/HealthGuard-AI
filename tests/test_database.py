from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import database.database as db_module
from database.database import Base
from database import models  # noqa: F401
from database.crud import create_patient, create_user, authenticate


def test_create_patient_and_user(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}", connect_args={'check_same_thread': False})
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)
    monkeypatch.setattr(db_module, 'SessionLocal', Session)

    patient = create_patient('Test User', 30, 'Other')
    user = create_user('test_unique_user', 'Password123!', 'patient', patient.id)
    assert patient.id is not None
    assert user is not None

    logged = authenticate('test_unique_user', 'Password123!')
    assert logged['patient_id'] == patient.id
