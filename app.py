import streamlit as st
from database.database import Base, engine
from database import models  # noqa: F401
from config import APP_NAME

st.set_page_config(page_title=APP_NAME, page_icon='🏥', layout='wide', initial_sidebar_state='expanded')
@st.cache_resource
def init_database():
    Base.metadata.create_all(bind=engine)

init_database()

st.markdown('''<style>
.block-container {padding-top: 2rem; max-width: 1250px;}
.login-card {max-width: 650px; margin: 4rem auto; padding: 2rem; border: 1px solid #ddd; border-radius: 18px;}
[data-testid="stMetric"] {border: 1px solid #e5e7eb; padding: 14px; border-radius: 12px;}
</style>''', unsafe_allow_html=True)

if 'user' not in st.session_state:
    from ui.login import render
    render(); st.stop()

user = st.session_state.user
patient_id = user.get('patient_id')
if not patient_id:
    st.error('This account is not linked to a patient profile.'); st.stop()

with st.sidebar:
    st.title('🏥 HealthGuard AI')
    st.caption(f"Signed in as **{user['username']}**")
    page = st.radio('Navigation', ['Dashboard','Medication','Nutrition','Medical Information','AI Assistant','Reports'])
    st.divider()
    if st.button('Log out', width='stretch'):
        st.session_state.clear(); st.rerun()

if page == 'Dashboard':
    from ui.dashboard import render; render(patient_id)
elif page == 'Medication':
    from ui.medication import render; render(patient_id)
elif page == 'Nutrition':
    from ui.nutrition import render; render(patient_id)
elif page == 'Medical Information':
    from ui.medical import render; render()
elif page == 'AI Assistant':
    from ui.chatbot import render; render(patient_id)
elif page == 'Reports':
    from ui.reports import render; render(patient_id)
