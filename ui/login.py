import streamlit as st
from auth.auth_service import login, register
from database.crud import create_patient

def render():
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.title('🏥 HealthGuard AI')
    st.caption('Personal healthcare monitoring dashboard')
    tab1, tab2 = st.tabs(['Login','Create account'])
    with tab1:
        username = st.text_input('Username', key='login_user')
        password = st.text_input('Password', type='password', key='login_pass')
        if st.button('Login', type='primary', use_container_width=True):
            user = login(username, password)
            if user:
                st.session_state.user = user; st.rerun()
            else: st.error('Invalid username or password.')
    with tab2:
        name = st.text_input('Full name', key='reg_name')
        age = st.number_input('Age', 1, 120, 18, key='reg_age')
        username = st.text_input('Choose username', key='reg_user')
        password = st.text_input('Choose password (8+ characters)', type='password', key='reg_pass')
        if st.button('Create patient account', use_container_width=True):
            if not name.strip() or len(username.strip()) < 3 or len(password) < 8:
                st.error('Enter a name, username of at least 3 characters, and password of at least 8 characters.')
            else:
                patient = create_patient(name.strip(), int(age), 'Prefer not to say')
                user = register(username, password, 'patient', patient.id)
                if user:
                    st.success('Account created. Please log in.')
                else:
                    st.error('That username is already in use.')
    st.markdown('</div>', unsafe_allow_html=True)
