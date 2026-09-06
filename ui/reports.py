import streamlit as st

from services.report_service import (
    report_data,
    metrics_csv,
    health_pdf,
)


def render(patient_id):

    # =========================================================
    # HEADER
    # =========================================================

    st.title("📊 Health Reports")

    st.caption(
        "Review your recorded health information and generate "
        "downloadable reports."
    )

    # =========================================================
    # LOAD REPORT DATA
    # =========================================================

    patient, metrics, medications, nutrition = report_data(
        patient_id
    )

    if not patient:

        st.error(
            "Patient profile not found."
        )

        return

    # =========================================================
    # PATIENT OVERVIEW
    # =========================================================

    st.html(
        f"""
        <div style="
            padding:1.3rem 1.4rem;
            border-radius:20px;
            background:linear-gradient(
                135deg,
                rgba(15,76,92,0.08),
                rgba(59,130,246,0.05)
            );
            border:1px solid rgba(15,76,92,0.12);
            margin:0.8rem 0 1.3rem 0;
        ">

            <div style="
                display:flex;
                align-items:center;
                gap:1rem;
            ">

                <div style="
                    width:56px;
                    height:56px;
                    border-radius:16px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:white;
                    font-size:1.9rem;
                    box-shadow:0 3px 10px rgba(15,76,92,0.08);
                ">
                    👤
                </div>

                <div>

                    <div style="
                        font-size:1.2rem;
                        font-weight:750;
                        color:#0f4c5c;
                    ">
                        {patient.name}
                    </div>

                    <div style="
                        margin-top:0.25rem;
                        color:#64748b;
                        font-size:0.9rem;
                    ">
                        Patient age: {patient.age}
                    </div>

                </div>

            </div>

        </div>
        """
    )

    # =========================================================
    # REPORT OVERVIEW
    # =========================================================

    st.subheader("📋 Report overview")

    metric_count = len(metrics) if metrics else 0
    medication_count = len(medications) if medications else 0
    nutrition_count = len(nutrition) if nutrition else 0

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "❤️ Health entries",
            metric_count,
        )

    with c2:
        st.metric(
            "💊 Medications",
            medication_count,
        )

    with c3:
        st.metric(
            "🥗 Nutrition entries",
            nutrition_count,
        )

    st.write("")

    # =========================================================
    # DOWNLOAD REPORTS
    # =========================================================

    st.subheader("📥 Download reports")

    st.caption(
        "Export your recorded health information for your own "
        "reference or to share with a healthcare professional."
    )

    csv_bytes = metrics_csv(metrics)

    pdf_bytes = health_pdf(
        patient,
        metrics,
        medications,
    )

    csv_col, pdf_col = st.columns(2)

    with csv_col:

        st.html(
            """
            <div style="
                padding:1.2rem;
                border:1px solid #e2e8f0;
                border-radius:18px;
                background:white;
                margin-bottom:0.7rem;
            ">

                <div style="
                    font-size:1.25rem;
                    font-weight:700;
                    color:#0f4c5c;
                ">
                    📈 Health Metrics
                </div>

                <div style="
                    margin-top:0.4rem;
                    color:#64748b;
                    font-size:0.88rem;
                ">
                    Download your recorded health measurements
                    in spreadsheet-friendly CSV format.
                </div>

            </div>
            """
        )

        st.download_button(
            "⬇️ Download CSV",
            csv_bytes,
            "health_metrics.csv",
            "text/csv",
            width="stretch",
        )

    with pdf_col:

        st.html(
            """
            <div style="
                padding:1.2rem;
                border:1px solid #e2e8f0;
                border-radius:18px;
                background:white;
                margin-bottom:0.7rem;
            ">

                <div style="
                    font-size:1.25rem;
                    font-weight:700;
                    color:#0f4c5c;
                ">
                    📄 Health Report
                </div>

                <div style="
                    margin-top:0.4rem;
                    color:#64748b;
                    font-size:0.88rem;
                ">
                    Generate a PDF summary containing your
                    health information and medications.
                </div>

            </div>
            """
        )

        st.download_button(
            "⬇️ Download PDF",
            pdf_bytes,
            "health_report.pdf",
            "application/pdf",
            width="stretch",
        )

    # =========================================================
    # DATA PREVIEW
    # =========================================================

    if metrics:

        st.divider()

        st.subheader("📊 Health data preview")

        st.caption(
            "A quick view of the health information included "
            "in your downloadable report."
        )

        # Show a simple summary without changing the report service.
        latest = metrics[-1]

        latest_date = getattr(
            latest,
            "metric_date",
            None,
        )

        if latest_date is None:
            latest_date = getattr(
                latest,
                "date",
                "Latest entry",
            )

        p1, p2, p3, p4 = st.columns(4)

        with p1:
            st.metric(
                "👟 Steps",
                getattr(latest, "steps", 0),
            )

        with p2:
            st.metric(
                "🔥 Calories",
                getattr(latest, "calories_burned", 0),
            )

        with p3:
            st.metric(
                "😴 Sleep",
                f"{getattr(latest, 'sleep_hours', 0)} h",
            )

        with p4:
            st.metric(
                "❤️ Heart rate",
                f"{getattr(latest, 'heart_rate', 0)} bpm",
            )

        st.caption(
            f"Latest recorded entry: {latest_date}"
        )

    else:

        st.html(
            """
            <div style="
                padding:2rem 1.5rem;
                text-align:center;
                border:1px dashed #cbd5e1;
                border-radius:20px;
                background:linear-gradient(
                    135deg,
                    rgba(15,76,92,0.03),
                    rgba(255,255,255,0.8)
                );
                margin-top:1rem;
            ">

                <div style="
                    font-size:2.7rem;
                    margin-bottom:0.5rem;
                ">
                    📊
                </div>

                <div style="
                    font-size:1.15rem;
                    font-weight:700;
                    color:#0f4c5c;
                ">
                    No health metrics recorded yet
                </div>

                <div style="
                    color:#64748b;
                    margin-top:0.4rem;
                    font-size:0.9rem;
                ">
                    Add health entries from your Dashboard
                    to build a more useful report.
                </div>

            </div>
            """
        )

    # =========================================================
    # REPORT CONTENT
    # =========================================================

    st.divider()

    st.subheader("📦 What's included")

    i1, i2, i3 = st.columns(3)

    with i1:

        st.html(
            """
            <div style="
                padding:1rem;
                border-radius:16px;
                background:#f8fafc;
                border:1px solid #e2e8f0;
                min-height:110px;
            ">

                <div style="font-size:1.5rem;">
                    ❤️
                </div>

                <div style="
                    font-weight:700;
                    color:#0f4c5c;
                    margin-top:0.35rem;
                ">
                    Health metrics
                </div>

                <div style="
                    color:#64748b;
                    font-size:0.82rem;
                    margin-top:0.25rem;
                ">
                    Recorded daily health measurements.
                </div>

            </div>
            """
        )

    with i2:

        st.html(
            """
            <div style="
                padding:1rem;
                border-radius:16px;
                background:#f8fafc;
                border:1px solid #e2e8f0;
                min-height:110px;
            ">

                <div style="font-size:1.5rem;">
                    💊
                </div>

                <div style="
                    font-weight:700;
                    color:#0f4c5c;
                    margin-top:0.35rem;
                ">
                    Medications
                </div>

                <div style="
                    color:#64748b;
                    font-size:0.82rem;
                    margin-top:0.25rem;
                ">
                    Medications associated with your profile.
                </div>

            </div>
            """
        )

    with i3:

        st.html(
            """
            <div style="
                padding:1rem;
                border-radius:16px;
                background:#f8fafc;
                border:1px solid #e2e8f0;
                min-height:110px;
            ">

                <div style="font-size:1.5rem;">
                    📄
                </div>

                <div style="
                    font-weight:700;
                    color:#0f4c5c;
                    margin-top:0.35rem;
                ">
                    Portable reports
                </div>

                <div style="
                    color:#64748b;
                    font-size:0.82rem;
                    margin-top:0.25rem;
                ">
                    Downloadable CSV and PDF formats.
                </div>

            </div>
            """
        )

    # =========================================================
    # DISCLAIMER
    # =========================================================

    st.divider()

    st.html(
        """
        <div style="
            padding:1rem 1.2rem;
            border-radius:14px;
            border:1px solid #dbe3e8;
            background:#f8fafb;
            color:#64748b;
            font-size:0.82rem;
        ">

            🛡️ <strong>HealthGuard AI reminder:</strong>
            Reports organize recorded information for monitoring
            and educational purposes. They are not intended to
            diagnose conditions or replace professional medical advice.

        </div>
        """
    )