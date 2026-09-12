import streamlit as st
from datetime import datetime, time, date

from database.crud import (
    add_medication,
    list_medications,
    delete_medication,
    mark_dose,
    dose_statuses,
)

from services.medication_interactions import check_medication_interactions


def render(patient_id):

    # =========================================================
    # HEADER
    # =========================================================

    st.title("💊 Medication Tracker")

    st.caption(
        "Keep your daily medications organized and track each dose with ease."
    )

    st.info(
        "💡 Reminders appear in the app when their scheduled time is reached. "
        "This prototype does not run background processes or send SMS/email alerts."
    )
    
    
    

    # =========================================================
    # ADD MEDICATION
    # =========================================================

    st.subheader("➕ Add a medication")

    with st.form("add_med"):

        a, b, c = st.columns(3)

        with a:
            name = st.text_input(
                "Medicine name",
                placeholder="e.g. Vitamin D",
            )

        with b:
            dosage = st.text_input(
                "Dosage",
                placeholder="e.g. 1 tablet",
            )

        with c:
            reminder = st.time_input(
                "Daily time",
                value=time(9, 0),
            )

        add_button = st.form_submit_button(
            "➕ Add medication",
            type="primary",
            width="stretch",
        )

        if add_button:

            if name.strip() and dosage.strip():

                add_medication(
                    patient_id,
                    name.strip(),
                    dosage.strip(),
                    reminder,
                )

                st.success("✅ Medication added successfully!")
                st.rerun()

            else:

                st.error(
                    "Please enter both the medicine name and dosage."
                )

    st.divider()
    st.subheader("Medication Safety Check")

    st.caption(
        "Check available FDA drug-label interaction information for your medications. "
        "This is informational only and does not replace advice from a doctor or pharmacist."
    )
    
    current_medications = list_medications(patient_id, active_only=True)
    
    medicine_names = [
        medication.medicine_name
        for medication in current_medications
    ]
    
    if medicine_names:
        if st.button("Check medication interactions", use_container_width=True):
            with st.spinner("Checking medication safety information..."):
                safety_results = check_medication_interactions(medicine_names)
    
            st.session_state["medication_safety_results"] = safety_results
    
    if "medication_safety_results" in st.session_state:
        st.markdown("### Safety information")
    
        for result in st.session_state["medication_safety_results"]:
            st.markdown(f"**{result['medicine']}**")
    
            if result["found"] and result["interactions"]:
                st.warning(
                    "FDA drug-label interaction information is available for this medicine."
                )
    
                for interaction in result["interactions"]:
                    st.write(interaction)
    
            elif result["found"]:
                st.info(
                    "No specific interaction information was returned in the "
                    "FDA drug label retrieved for this medicine."
                )
    
            else:
                st.warning(result["message"])
    
            st.caption("Source: openFDA / FDA drug labeling")

    # =========================================================
    # TODAY'S MEDICATIONS
    # =========================================================

    st.subheader("📅 Today's schedule")

    meds = list_medications(
        patient_id,
        active_only=True,
    )

    now = datetime.now().time()

    statuses = dose_statuses(
        patient_id,
        date.today(),
    )

    # =========================================================
    # EMPTY STATE
    # =========================================================

    if not meds:

        st.html(
            """
            <div style="
                padding:2.5rem 1.5rem;
                text-align:center;
                border:1px dashed #cbd5e1;
                border-radius:20px;
                background:linear-gradient(
                    135deg,
                    rgba(15,76,92,0.04),
                    rgba(255,255,255,0.8)
                );
                margin-top:1rem;
            ">

                <div style="
                    font-size:3rem;
                    margin-bottom:0.5rem;
                ">
                    💊
                </div>

                <div style="
                    font-size:1.25rem;
                    font-weight:700;
                    color:#0f4c5c;
                ">
                    No medications yet
                </div>

                <div style="
                    color:#64748b;
                    margin-top:0.4rem;
                    font-size:0.95rem;
                ">
                    Add your first medication above to start
                    tracking today's schedule.
                </div>

            </div>
            """
        )

        return

    # =========================================================
    # SUMMARY
    # =========================================================

    taken_count = sum(
        1
        for med in meds
        if statuses.get(med.id) == "taken"
    )

    total_count = len(meds)

    remaining_count = total_count - taken_count

    summary1, summary2, summary3 = st.columns(3)

    with summary1:
        st.metric(
            "💊 Medications",
            total_count,
        )

    with summary2:
        st.metric(
            "✅ Taken",
            taken_count,
        )

    with summary3:
        st.metric(
            "⏳ Remaining",
            remaining_count,
        )

    st.write("")

    # =========================================================
    # MEDICATION CARDS
    # =========================================================

    for med in meds:

        status = statuses.get(
            med.id,
            "pending",
        )

        # -----------------------------------------------------
        # Determine visual status
        # -----------------------------------------------------

        if status == "taken":

            status_label = "✓ Taken"
            status_bg = "#ecfdf5"
            status_color = "#047857"

        elif now >= med.reminder_time:

            status_label = "⚠ Due"
            status_bg = "#fff7ed"
            status_color = "#c2410c"

        else:

            status_label = "◷ Upcoming"
            status_bg = "#eff6ff"
            status_color = "#1d4ed8"

        # -----------------------------------------------------
        # Card
        # -----------------------------------------------------

        st.html(
            f"""
            <div style="
                border:1px solid #e2e8f0;
                border-radius:18px;
                padding:1.2rem;
                margin:0.6rem 0 0.2rem 0;
                background:white;
                box-shadow:0 3px 12px rgba(15,76,92,0.05);
            ">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    gap:1rem;
                ">

                    <div>

                        <div style="
                            font-size:1.1rem;
                            font-weight:700;
                            color:#0f4c5c;
                        ">
                            💊 {med.medicine_name}
                        </div>

                        <div style="
                            color:#64748b;
                            margin-top:0.25rem;
                        ">
                            {med.dosage}
                        </div>

                    </div>

                    <div style="
                        padding:0.35rem 0.7rem;
                        border-radius:999px;
                        background:{status_bg};
                        color:{status_color};
                        font-size:0.82rem;
                        font-weight:700;
                        white-space:nowrap;
                    ">
                        {status_label}
                    </div>

                </div>

                <div style="
                    margin-top:0.8rem;
                    padding-top:0.7rem;
                    border-top:1px solid #f1f5f9;
                    color:#64748b;
                    font-size:0.9rem;
                ">
                    🕐 Scheduled for
                    <strong style="color:#334155;">
                        {med.reminder_time.strftime("%I:%M %p")}
                    </strong>
                </div>

            </div>
            """
        )

        # -----------------------------------------------------
        # Actions
        # -----------------------------------------------------

        action1, action2, action3 = st.columns(
            [1, 1, 4]
        )

        if status != "taken":

            with action1:

                if st.button(
                    "✓ Mark taken",
                    key=f"take_{med.id}",
                    width="stretch",
                ):

                    mark_dose(
                        med.id,
                        patient_id,
                    )

                    st.success(
                        f"✅ {med.medicine_name} marked as taken."
                    )

                    st.rerun()

        else:

            with action1:

                st.success("Taken")

        with action2:

            if st.button(
                "🗑 Delete",
                key=f"del_{med.id}",
                width="stretch",
            ):

                delete_medication(
                    med.id,
                    patient_id,
                )

                st.success(
                    f"🗑 {med.medicine_name} removed."
                )

                st.rerun()

        st.write("")

    # =========================================================
    # FOOTER
    # =========================================================

    st.divider()

    st.caption(
        "HealthGuard AI helps you organize health information. "
        "Always follow medication instructions provided by your healthcare professional."
    )
