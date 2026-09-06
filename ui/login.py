import streamlit as st

from auth.auth_service import login, register
from database.crud import create_patient


def render():
    # Show success message after registration refresh
    registration_success = st.session_state.pop(
        "registration_success",
        False,
    )

    # Page styling
    st.markdown(
        """
        <style>
        .login-title {
            text-align: center;
            color: #0f4c5c;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .login-subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 2rem;
        }

        .feature-box {
            text-align: center;
            padding: 1rem;
            border: 1px solid #e2e8f0;
            border-radius: 15px;
            background: #f8fafc;
        }

        .feature-icon {
            font-size: 1.8rem;
        }

        .feature-title {
            color: #0f4c5c;
            font-weight: 700;
            margin-top: 0.4rem;
        }

        .feature-text {
            color: #64748b;
            font-size: 0.8rem;
        }

        .footer-text {
            text-align: center;
            color: #94a3b8;
            font-size: 0.8rem;
            margin-top: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ============================================================
    # HEADER
    # ============================================================

    st.markdown(
        '<div class="login-title">🏥 HealthGuard AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="login-subtitle">'
        'Your personal healthcare monitoring dashboard'
        '</div>',
        unsafe_allow_html=True,
    )

    # ============================================================
    # LOGIN / REGISTER TABS
    # ============================================================

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "✨ Create Account"]
    )

    # ============================================================
    # LOGIN
    # ============================================================

    with login_tab:

        st.subheader("Welcome back")

        st.caption(
            "Sign in to continue to your HealthGuard dashboard."
        )

        username = st.text_input(
            "Username",
            key="login_user",
            placeholder="Enter your username",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_pass",
            placeholder="Enter your password",
        )

        st.write("")

        if st.button(
            "🔓 Login to HealthGuard",
            type="primary",
            width="stretch",
        ):

            if not username.strip():
                st.warning("Please enter your username.")

            elif not password:
                st.warning("Please enter your password.")

            else:
                user = login(
                    username.strip(),
                    password,
                )

                if user:
                    st.session_state.user = user
                    st.rerun()

                else:
                    st.error(
                        "❌ Invalid username or password."
                    )

    # ============================================================
    # CREATE ACCOUNT
    # ============================================================

    with register_tab:

        if registration_success:
            st.success(
                "✅ Account created successfully! "
                "You can now log in with your new account."
            )

        st.subheader("Create your account")

        st.caption(
            "Create a patient account to start using "
            "HealthGuard AI."
        )

        name = st.text_input(
            "Full name",
            key="reg_name",
            placeholder="Enter your full name",
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18,
            key="reg_age",
        )

        new_username = st.text_input(
            "Choose username",
            key="reg_user",
            placeholder="At least 3 characters",
        )

        new_password = st.text_input(
            "Choose password",
            type="password",
            key="reg_pass",
            placeholder="At least 8 characters",
        )

        st.caption(
            "🔒 Password must contain at least 8 characters."
        )

        st.write("")

        if st.button(
            "🚀 Create Patient Account",
            type="primary",
            width="stretch",
        ):

            # Validate input
            if not name.strip():

                st.error(
                    "Please enter your full name."
                )

            elif len(new_username.strip()) < 3:

                st.error(
                    "Username must be at least 3 characters."
                )

            elif len(new_password) < 8:

                st.error(
                    "Password must be at least 8 characters."
                )

            else:

                # Create patient profile
                patient = create_patient(
                    name.strip(),
                    int(age),
                    "Prefer not to say",
                )

                # Create user account
                user = register(
                    new_username.strip(),
                    new_password,
                    "patient",
                    patient.id,
                )

                if user:

                    # Clear registration fields
                    st.session_state.pop(
                        "reg_name",
                        None,
                    )

                    st.session_state.pop(
                        "reg_age",
                        None,
                    )

                    st.session_state.pop(
                        "reg_user",
                        None,
                    )

                    st.session_state.pop(
                        "reg_pass",
                        None,
                    )

                    # Set success flag
                    st.session_state[
                        "registration_success"
                    ] = True

                    # Refresh application
                    st.rerun()

                else:

                    st.error(
                        "❌ That username is already in use."
                    )

    # ============================================================
    # FEATURES
    # ============================================================

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-box">
                <div class="feature-icon">💊</div>
                <div class="feature-title">
                    Medication
                </div>
                <div class="feature-text">
                    Track your daily medicines
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-box">
                <div class="feature-icon">📊</div>
                <div class="feature-title">
                    Health Insights
                </div>
                <div class="feature-text">
                    Monitor your health trends
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="feature-box">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">
                    AI Assistant
                </div>
                <div class="feature-text">
                    Get educational health guidance
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ============================================================
    # FOOTER
    # ============================================================

    st.markdown(
        """
        <div class="footer-text">
            HealthGuard AI provides educational health information
            and monitoring tools. It does not replace professional
            medical advice.
        </div>
        """,
        unsafe_allow_html=True,
    )