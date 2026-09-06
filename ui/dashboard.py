import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database.crud import get_patient, list_metrics, add_metric
from services.analytics import adherence_percentage, nutrition_totals


def render(patient_id):
    patient = get_patient(patient_id)

    if not patient:
        st.error('Patient record not found.')
        return

    # ---------- Header ----------
    st.markdown(
        """
        <div style="
            padding: 1.5rem 1.8rem;
            border-radius: 18px;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #0f4c5c, #1b7a8f);
            color: white;
        ">
            <div style="font-size: 0.9rem; opacity: 0.85;">
                HEALTHGUARD AI • PERSONAL HEALTH DASHBOARD
            </div>
            <div style="font-size: 2rem; font-weight: 700; margin-top: 0.3rem;">
                Welcome back, {name} 👋
            </div>
            <div style="font-size: 1rem; opacity: 0.9; margin-top: 0.4rem;">
                Monitor your daily health habits and stay informed.
            </div>
        </div>
        """.format(name=patient.name),
        unsafe_allow_html=True,
    )

    # ---------- Data ----------
    metrics = list_metrics(patient_id)
    totals = nutrition_totals(patient_id)
    adherence = adherence_percentage(patient_id)

    latest_metric = metrics[-1] if metrics else None

    # ---------- KPI Cards ----------
    st.subheader('Today at a glance')

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        '💊 Medication',
        f'{adherence:.0f}%',
        'Adherence',
    )

    c2.metric(
        '👟 Steps',
        f'{latest_metric.steps:,}' if latest_metric else '—',
        'Latest entry',
    )

    c3.metric(
        '😴 Sleep',
        f'{latest_metric.sleep_hours:.1f} h' if latest_metric else '—',
        'Latest entry',
    )

    c4.metric(
        '🔥 Calories',
        f"{totals['calories']:.0f}",
        'Today',
    )

    c5.metric(
        '🥩 Protein',
        f"{totals['protein_g']:.1f} g",
        'Today',
    )

    st.divider()

    # ---------- Health Status ----------
    st.subheader('Health snapshot')

    status_cols = st.columns(3)

    if adherence >= 80:
        status_cols[0].success('💊 Medication adherence looks good')
    elif adherence > 0:
        status_cols[0].warning('💊 Medication adherence could improve')
    else:
        status_cols[0].info('💊 No medication data yet')

    if latest_metric and latest_metric.sleep_hours >= 7:
        status_cols[1].success('😴 Sleep entry is in a healthy range')
    elif latest_metric:
        status_cols[1].warning('😴 Consider monitoring your sleep')
    else:
        status_cols[1].info('😴 Add a sleep entry')

    if latest_metric and latest_metric.steps >= 5000:
        status_cols[2].success('👟 Good activity recorded')
    elif latest_metric:
        status_cols[2].info('👟 Keep building your daily activity')
    else:
        status_cols[2].info('👟 Add your activity data')

    st.divider()

    # ---------- Add Metrics ----------
    st.subheader("➕ Record today's health metrics")

    with st.form("metrics_form"):
        a, b, c, d = st.columns(4)

        metric_date = a.date_input(
            "Date",
            value=date.today(),
        )

        steps = b.number_input(
            "Steps",
            min_value=0,
            step=100,
        )

        calories = c.number_input(
            "Calories burned",
            min_value=0.0,
            step=10.0,
        )

        sleep = d.number_input(
            "Sleep hours",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
        )

        heart = st.number_input(
            "Heart rate (bpm)",
            min_value=0,
            max_value=250,
            value=70,
        )

        submitted = st.form_submit_button(
            "Save health metrics",
            type="primary",
            width="stretch",
        )

        if submitted:
            add_metric(
                patient_id,
                metric_date,
                int(steps),
                float(calories),
                float(sleep),
                int(heart),
            )
            st.success("Health metrics saved successfully.")
            st.rerun()

    # ---------- Charts ----------
    if metrics:
        st.divider()
        st.subheader('📈 Your health trends')

        df = pd.DataFrame(
            [
                {
                    'Date': m.metric_date,
                    'Steps': m.steps,
                    'Sleep': m.sleep_hours,
                    'Heart Rate': m.heart_rate,
                }
                for m in metrics
            ]
        )

        chart1, chart2 = st.columns(2)

        with chart1:
            fig_steps = px.line(
                df,
                x='Date',
                y='Steps',
                markers=True,
                title='Daily steps',
            )
            fig_steps.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=60, b=20),
                hovermode='x unified',
            )
            st.plotly_chart(
                fig_steps,
                width='stretch',
            )

        with chart2:
            fig_sleep = px.line(
                df,
                x='Date',
                y='Sleep',
                markers=True,
                title='Sleep duration',
            )
            fig_sleep.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=60, b=20),
                hovermode='x unified',
            )
            st.plotly_chart(
                fig_sleep,
                width='stretch',
            )

        st.subheader('❤️ Heart-rate history')

        fig_hr = px.line(
            df,
            x='Date',
            y='Heart Rate',
            markers=True,
            title='Recorded heart rate',
        )

        fig_hr.update_layout(
            height=330,
            margin=dict(l=20, r=20, t=60, b=20),
            hovermode='x unified',
        )

        st.plotly_chart(
            fig_hr,
            width='stretch',
        )

    else:
        st.info(
            '📊 No health metrics recorded yet. '
            'Add your first entry above to start seeing your trends.'
        )

    # ---------- Nutrition ----------
    st.divider()
    st.subheader('🥗 Nutrition today')

    n1, n2, n3, n4 = st.columns(4)

    n1.metric('Calories', f"{totals['calories']:.0f} kcal")
    n2.metric('Protein', f"{totals['protein_g']:.1f} g")
    n3.metric('Carbohydrates', f"{totals['carbs_g']:.1f} g")
    n4.metric('Fat', f"{totals['fat_g']:.1f} g")

    # ---------- Disclaimer ----------
    st.markdown(
        """
        <div style="
            margin-top: 2rem;
            padding: 1rem 1.2rem;
            border-radius: 12px;
            border: 1px solid #ddd;
            font-size: 0.82rem;
            opacity: 0.8;
        ">
            🛡️ <strong>HealthGuard AI reminder:</strong>
            This application provides educational health monitoring information.
            It does not diagnose, treat, or replace advice from a qualified
            healthcare professional.
        </div>
        """,
        unsafe_allow_html=True,
    )
    