from database.database import Base, engine
from database import models  # noqa: F401

Base.metadata.create_all(bind=engine)
print('Database initialized successfully.')
