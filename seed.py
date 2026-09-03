from database.database import Base, engine
from database import models  # noqa
from database.crud import create_patient, create_user, add_medication, add_metric
from datetime import date, time

Base.metadata.create_all(bind=engine)

patient = create_patient('Demo User', 22, 'Prefer not to say', 175, 70)
create_user('demo', 'DemoPass123!', 'patient', patient.id)
add_medication(patient.id, 'Vitamin D', '1 tablet', time(9, 0))
add_medication(patient.id, 'Sample Medicine', '1 tablet', time(20, 0))
add_metric(patient.id, date.today(), 6500, 420, 7.5, 72)
print('Demo account created: username=demo password=DemoPass123!')
