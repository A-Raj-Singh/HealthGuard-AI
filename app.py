import streamlit as st

from database.database import Base, engine
from database import models  # noqa: F401
from config import APP_NAME


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

@st.cache_resource
def init_database():
    from database import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


init_database()


# =========================================================
# GLOBAL UI STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(15, 76, 92, 0.12);
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 16px;
        min-height: 115px;
        box-shadow: 0 2px 8px rgba(15, 76, 92, 0.05);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    /* Forms */
    [data-testid="stForm"] {
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.2rem;
        background: rgba(255, 255, 255, 0.65);
    }

    /* Expanders */
    [data-testid="stExpander"] {
        border-radius: 14px;
        border: 1px solid #e5e7eb;
    }

    /* HealthGuard cards */
    .hg-card {
        background: linear-gradient(
            135deg,
            rgba(15, 76, 92, 0.06),
            rgba(255, 255, 255, 0.95)
        );
        border: 1px solid rgba(15, 76, 92, 0.12);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(15, 76, 92, 0.06);
    }

    /* Hide Streamlit chrome */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LOGIN CHECK
# =========================================================

if "user" not in st.session_state:
    from ui.login import render

    render()
    st.stop()


user = st.session_state.user

patient_id = user.get("patient_id")

if not patient_id:
    st.error("This account is not linked to a patient profile.")
    st.stop()


# =========================================================
# APPLICATION PAGES
# =========================================================

pages = [
    "Dashboard",
    "Medication",
    "Nutrition",
    "Goals",
    "Medical Information",
    "AI Assistant",
    "Reports",
]


# =========================================================
# NAVIGATION STATE
# =========================================================

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Dashboard"


# Quick Action buttons use this temporary request.
# This prevents conflicts with the sidebar radio widget.
if "navigation_request" in st.session_state:
    st.session_state.nav_page = st.session_state.navigation_request
    del st.session_state.navigation_request


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # -----------------------------------------------------
    # BRANDING
    # -----------------------------------------------------

    st.html(
        """
        <div style="
            padding:0.4rem 0 1rem 0;
        ">

            <div style="
                font-size:1.45rem;
                font-weight:750;
                color:#0f4c5c;
            ">
                🏥 HealthGuard AI
            </div>

            <div style="
                color:#64748b;
                font-size:0.82rem;
                margin-top:0.2rem;
            ">
                Personal Health Command Center
            </div>

        </div>
        """
    )


    # -----------------------------------------------------
    # USER CARD
    # -----------------------------------------------------

    st.html(
        f"""
        <div style="
            padding:0.8rem;
            border-radius:12px;
            background:rgba(15,76,92,0.06);
            margin-bottom:1rem;
        ">

            <div style="
                font-size:0.75rem;
                color:#64748b;
            ">
                SIGNED IN AS
            </div>

            <div style="
                font-weight:650;
                color:#0f4c5c;
                margin-top:0.15rem;
            ">
                👤 {user["username"]}
            </div>

        </div>
        """
    )


    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------

    selected_page = st.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state.nav_page),
        label_visibility="collapsed",
    )


    # Sidebar navigation
    if selected_page != st.session_state.nav_page:
        st.session_state.nav_page = selected_page
        st.rerun()


    # -----------------------------------------------------
    # SIDEBAR FOOTER
    # -----------------------------------------------------

    st.divider()

    st.caption("Your health, organized.")


    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    if st.button(
        "🚪 Log out",
        width="stretch",
    ):
        st.session_state.clear()
        st.rerun()


# =========================================================
# CURRENT PAGE
# =========================================================

page = st.session_state.nav_page


# =========================================================
# PAGE ROUTING
# =========================================================

if page == "Dashboard":

    from ui.dashboard import render

    render(patient_id)


elif page == "Medication":

    from ui.medication import render

    render(patient_id)


elif page == "Nutrition":

    from ui.nutrition import render

    render(patient_id)


elif page == "Medical Information":

    from ui.medical import render

    render()


elif page == "AI Assistant":

    from ui.chatbot import render

    render(patient_id)

elif page == "Goals":

    from ui.goals import render

    render(patient_id)


elif page == "Reports":

    from ui.reports import render

    render(patient_id)
