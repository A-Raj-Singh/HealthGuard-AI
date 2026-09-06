import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database.crud import (
    get_patient,
    list_metrics,
    add_metric,
)
from services.analytics import (
    adherence_percentage,
    nutrition_totals,
)


def render(patient_id):

    patient = get_patient(patient_id)

    if not patient:
        st.error("Patient record not found.")
        return

    # ============================================================
    # DATA
    # ============================================================

    metrics = list_metrics(patient_id)
    totals = nutrition_totals(patient_id)
    adherence = adherence_percentage(patient_id)

    latest_metric = metrics[-1] if metrics else None

    # Initialize health form state
    if "show_health_form" not in st.session_state:
        st.session_state.show_health_form = False

    # ============================================================
    # HERO
    # ============================================================

    st.html(
        f"""
<div style="
    padding:2rem 2.2rem;
    border-radius:22px;
    margin-bottom:1.5rem;
    background:linear-gradient(135deg,#0f4c5c,#176b7a,#1b7a8f);
    color:white;
    box-shadow:0 8px 24px rgba(15,76,92,0.18);
">
    <div style="
        font-size:0.78rem;
        font-weight:700;
        letter-spacing:1.5px;
        opacity:0.8;
    ">
        HEALTHGUARD AI
    </div>

    <div style="
        font-size:2.15rem;
        font-weight:750;
        margin-top:0.35rem;
    ">
        Welcome back, {patient.name} 👋
    </div>

    <div style="
        font-size:1rem;
        opacity:0.9;
        margin-top:0.5rem;
    ">
        Your personal health command center.
        Keep tracking, stay informed, and build healthy habits.
    </div>
</div>
"""
    )

    # ============================================================
    # QUICK ACTIONS
    # ============================================================

    st.subheader("⚡ Quick actions")

    q1, q2, q3, q4 = st.columns(4)

    if q1.button("💊 Medication", width="stretch"):
        st.session_state.nav_page = "Medication"
        st.session_state.show_health_form = False
        st.rerun()

    if q2.button("🥗 Add nutrition", width="stretch"):
        st.session_state.nav_page = "Nutrition"
        st.session_state.show_health_form = False
        st.rerun()

    if q3.button("❤️ Health entry", width="stretch"):
        st.session_state.show_health_form = True
        st.rerun()

    if q4.button("🤖 Ask AI", width="stretch"):
        st.session_state.nav_page = "AI Assistant"
        st.session_state.show_health_form = False
        st.rerun()

    # ============================================================
    # HEALTH ENTRY
    # ============================================================

    if st.session_state.show_health_form:

        st.divider()

        st.subheader("❤️ Record today's health")

        st.info(
            "Add your daily activity, sleep, calories and heart-rate information."
        )

        with st.form("health_entry_form"):

            col1, col2 = st.columns(2)

            with col1:

                metric_date = st.date_input(
                    "📅 Date",
                    value=date.today(),
                )

                steps = st.number_input(
                    "👟 Steps",
                    min_value=0,
                    step=100,
                    value=0,
                )

                calories = st.number_input(
                    "🔥 Calories burned",
                    min_value=0.0,
                    step=10.0,
                    value=0.0,
                )

            with col2:

                sleep = st.number_input(
                    "😴 Sleep hours",
                    min_value=0.0,
                    max_value=24.0,
                    step=0.5,
                    value=0.0,
                )

                heart = st.number_input(
                    "❤️ Heart rate (bpm)",
                    min_value=0,
                    max_value=250,
                    step=1,
                    value=70,
                )

            save_col, cancel_col = st.columns(2)

            with save_col:

                save_health = st.form_submit_button(
                    "💾 Save health entry",
                    type="primary",
                    width="stretch",
                )

            with cancel_col:

                cancel_health = st.form_submit_button(
                    "✕ Cancel",
                    width="stretch",
                )

        if save_health:

            add_metric(
                patient_id,
                metric_date,
                int(steps),
                float(calories),
                float(sleep),
                int(heart),
            )

            st.session_state.show_health_form = False

            st.success("✅ Health entry saved successfully!")

            st.rerun()

        if cancel_health:

            st.session_state.show_health_form = False

            st.rerun()

    # ============================================================
    # TODAY'S OVERVIEW
    # ============================================================

    st.divider()

    st.subheader("📊 Today's overview")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "💊 Medication",
        f"{adherence:.0f}%",
        "Adherence today",
    )

    c2.metric(
        "👟 Steps",
        f"{latest_metric.steps:,}"
        if latest_metric
        else "—",
        "Latest recorded",
    )

    c3.metric(
        "😴 Sleep",
        f"{latest_metric.sleep_hours:.1f} h"
        if latest_metric
        else "—",
        "Latest recorded",
    )

    c4.metric(
        "🔥 Calories",
        f"{totals['calories']:.0f}",
        "Today's nutrition",
    )

    c5.metric(
        "🥩 Protein",
        f"{totals['protein_g']:.1f} g",
        "Today's nutrition",
    )

    # ============================================================
    # TRACKING SCORE
    # ============================================================

    score_items = 0
    completed_items = 0

    if adherence > 0:

        score_items += 1

        if adherence >= 80:
            completed_items += 1

    if latest_metric:

        score_items += 2

        if latest_metric.steps > 0:
            completed_items += 1

        if latest_metric.sleep_hours > 0:
            completed_items += 1

    if totals["calories"] > 0:

        score_items += 1
        completed_items += 1

    if totals["protein_g"] > 0:

        score_items += 1
        completed_items += 1

    tracking_score = (
        round(completed_items / score_items * 100)
        if score_items
        else 0
    )

    st.html(
        f"""
<div style="
    margin-top:1.5rem;
    padding:1.25rem;
    border-radius:16px;
    border:1px solid #e5e7eb;
    background:rgba(255,255,255,0.8);
    box-shadow:0 2px 8px rgba(15,76,92,0.04);
">

    <div style="
        font-size:0.8rem;
        color:#64748b;
        font-weight:700;
        letter-spacing:0.8px;
    ">
        DAILY TRACKING SCORE
    </div>

    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-top:0.35rem;
    ">

        <div style="
            font-size:1.5rem;
            font-weight:700;
        ">
            {tracking_score}%
        </div>

        <div style="
            color:#64748b;
            font-size:0.85rem;
        ">
            Keep your health data updated
        </div>

    </div>

    <div style="
        height:9px;
        background:#e5e7eb;
        border-radius:20px;
        margin-top:0.7rem;
        overflow:hidden;
    ">

        <div style="
            width:{tracking_score}%;
            height:100%;
            background:linear-gradient(90deg,#0f4c5c,#36a6b9);
            border-radius:20px;
        "></div>

    </div>

</div>
"""
    )

    # ============================================================
    # HEALTH SNAPSHOT
    # ============================================================

    st.subheader("✨ Health snapshot")

    status_cols = st.columns(3)

    if adherence >= 80:

        status_cols[0].success(
            "💊 Medication tracking is on track."
        )

    elif adherence > 0:

        status_cols[0].warning(
            "💊 Some medication entries are still pending."
        )

    else:

        status_cols[0].info(
            "💊 Start tracking your medications."
        )

    if latest_metric and latest_metric.sleep_hours >= 7:

        status_cols[1].success(
            "😴 Your latest sleep entry is 7+ hours."
        )

    elif latest_metric:

        status_cols[1].info(
            "😴 Keep recording your sleep consistently."
        )

    else:

        status_cols[1].info(
            "😴 Record your sleep to build a trend."
        )

    if latest_metric and latest_metric.steps >= 5000:

        status_cols[2].success(
            "👟 You've recorded a strong activity level."
        )

    elif latest_metric:

        status_cols[2].info(
            "👟 Keep building your daily activity."
        )

    else:

        status_cols[2].info(
            "👟 Record your activity to start tracking."
        )

    # ============================================================
    # HEALTH TRENDS
    # ============================================================

    if metrics:

        st.divider()

        st.subheader("📈 Your health trends")

        df = pd.DataFrame(
            [
                {
                    "Date": m.metric_date,
                    "Steps": m.steps,
                    "Sleep": m.sleep_hours,
                    "Heart Rate": m.heart_rate,
                }
                for m in metrics
            ]
        )

        chart1, chart2 = st.columns(2)

        with chart1:

            fig_steps = px.line(
                df,
                x="Date",
                y="Steps",
                markers=True,
                title="👟 Daily steps",
            )

            fig_steps.update_layout(
                height=350,
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20,
                ),
                hovermode="x unified",
            )

            st.plotly_chart(
                fig_steps,
                width="stretch",
            )

        with chart2:

            fig_sleep = px.line(
                df,
                x="Date",
                y="Sleep",
                markers=True,
                title="😴 Sleep duration",
            )

            fig_sleep.update_layout(
                height=350,
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20,
                ),
                hovermode="x unified",
            )

            st.plotly_chart(
                fig_sleep,
                width="stretch",
            )

        st.subheader("❤️ Heart-rate history")

        fig_hr = px.line(
            df,
            x="Date",
            y="Heart Rate",
            markers=True,
            title="Recorded heart rate",
        )

        fig_hr.update_layout(
            height=330,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20,
            ),
            hovermode="x unified",
        )

        st.plotly_chart(
            fig_hr,
            width="stretch",
        )

    else:

        st.info(
            "📊 No health metrics recorded yet. "
            "Click **❤️ Health entry** above to add your first entry."
        )

    # ============================================================
    # NUTRITION SUMMARY
    # ============================================================

    st.divider()

    st.subheader("🥗 Nutrition today")

    n1, n2, n3, n4 = st.columns(4)

    n1.metric(
        "🔥 Calories",
        f"{totals['calories']:.0f} kcal",
    )

    n2.metric(
        "🥩 Protein",
        f"{totals['protein_g']:.1f} g",
    )

    n3.metric(
        "🍚 Carbohydrates",
        f"{totals['carbs_g']:.1f} g",
    )

    n4.metric(
        "🥑 Fat",
        f"{totals['fat_g']:.1f} g",
    )

    # ============================================================
    # DISCLAIMER
    # ============================================================

    st.html(
        """
<div style="
    margin-top:2rem;
    padding:1rem 1.2rem;
    border-radius:14px;
    border:1px solid #dbe3e8;
    background:#f8fafb;
    color:#64748b;
    font-size:0.82rem;
">
    🛡️ <strong>HealthGuard AI reminder:</strong>
    This application provides educational health monitoring
    information. It does not diagnose, treat, or replace advice
    from a qualified healthcare professional.
</div>
"""
    )