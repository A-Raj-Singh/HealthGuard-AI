from database.crud import authenticate, create_user

def register(username, password, role='patient', patient_id=None):
    if len(username.strip()) < 3 or len(password) < 8:
        return None
    return create_user(username, password, role, patient_id)

def login(username, password):
    return authenticate(username, password)
