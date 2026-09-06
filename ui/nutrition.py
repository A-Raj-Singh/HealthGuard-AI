import streamlit as st
import pandas as pd

from services.nutrition_service import analyze_and_save, history
from config import SPOONACULAR_API_KEY


def render(patient_id):

    # =========================================================
    # HEADER
    # =========================================================

    st.title("🥗 Nutrition Tracker")

    st.caption(
        "Track your meals, understand your nutrition, and build healthier daily habits."
    )

    # =========================================================
    # API STATUS
    # =========================================================

    if SPOONACULAR_API_KEY:
        st.success(
            "✨ Spoonacular nutrition lookup is enabled. "
            "Food analysis can use the connected nutrition service."
        )
    else:
        st.info(
            "💡 No Spoonacular key detected. "
            "You can still record nutrition manually."
        )

    # =========================================================
    # LOAD HISTORY
    # =========================================================

    logs = history(patient_id)

    # =========================================================
    # TODAY'S SUMMARY
    # =========================================================

    today_logs = [
        log for log in logs
        if log.log_date == pd.Timestamp.today().date()
    ]

    today_calories = sum(
        float(log.calories or 0)
        for log in today_logs
    )

    today_protein = sum(
        float(log.protein_g or 0)
        for log in today_logs
    )

    today_carbs = sum(
        float(log.carbs_g or 0)
        for log in today_logs
    )

    today_fat = sum(
        float(log.fat_g or 0)
        for log in today_logs
    )

    # =========================================================
    # NUTRITION SUMMARY CARDS
    # =========================================================

    st.subheader("📊 Today's nutrition")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            "🔥 Calories",
            f"{today_calories:.0f} kcal",
        )

    with s2:
        st.metric(
            "🥩 Protein",
            f"{today_protein:.1f} g",
        )

    with s3:
        st.metric(
            "🍚 Carbohydrates",
            f"{today_carbs:.1f} g",
        )

    with s4:
        st.metric(
            "🥑 Fat",
            f"{today_fat:.1f} g",
        )

    st.write("")

    # =========================================================
    # ADD FOOD / MEAL
    # =========================================================

    st.subheader("➕ Add a meal")

    with st.form("nutrition_form"):

        food = st.text_input(
            "Food / meal name",
            placeholder="e.g. Chicken rice bowl",
        )

        a, b, c = st.columns(3)

        with a:
            calories = st.number_input(
                "🔥 Calories",
                min_value=0.0,
                step=10.0,
                value=0.0,
            )

        with b:
            protein = st.number_input(
                "🥩 Protein (g)",
                min_value=0.0,
                step=1.0,
                value=0.0,
            )

        with c:
            carbs = st.number_input(
                "🍚 Carbs (g)",
                min_value=0.0,
                step=1.0,
                value=0.0,
            )

        fat = st.number_input(
            "🥑 Fat (g)",
            min_value=0.0,
            step=1.0,
            value=0.0,
        )

        save_food = st.form_submit_button(
            "✨ Analyze & save meal",
            type="primary",
            width="stretch",
        )

        if save_food:

            if food.strip():

                try:

                    obj = analyze_and_save(
                        patient_id,
                        food.strip(),
                        calories,
                        protein,
                        carbs,
                        fat,
                    )

                    st.success(
                        f"✅ {food.strip()} saved successfully using {obj.source}."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Unable to save this meal: {e}"
                    )

            else:

                st.error(
                    "Please enter a food or meal name."
                )

    st.divider()

    # =========================================================
    # EMPTY STATE
    # =========================================================

    if not logs:

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
                    🥗
                </div>

                <div style="
                    font-size:1.25rem;
                    font-weight:700;
                    color:#0f4c5c;
                ">
                    No meals recorded yet
                </div>

                <div style="
                    color:#64748b;
                    margin-top:0.4rem;
                    font-size:0.95rem;
                ">
                    Add your first meal above to start building
                    your nutrition history.
                </div>

            </div>
            """
        )

        # Educational reminder
        st.info(
            "💡 Tip: Recording meals consistently can help you understand "
            "your daily nutrition patterns."
        )

        return

    # =========================================================
    # NUTRITION HISTORY
    # =========================================================

    st.subheader("📋 Nutrition history")

    df = pd.DataFrame(
        [
            {
                "Date": log.log_date,
                "Food": log.food_name,
                "Calories": log.calories,
                "Protein (g)": log.protein_g,
                "Carbs (g)": log.carbs_g,
                "Fat (g)": log.fat_g,
                "Source": log.source,
            }
            for log in logs
        ]
    )

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
    )

    # =========================================================
    # RECENT MEALS
    # =========================================================

    st.subheader("🍽️ Recent meals")

    recent_logs = logs[:5]

    for log in recent_logs:

        calories_value = float(log.calories or 0)
        protein_value = float(log.protein_g or 0)
        carbs_value = float(log.carbs_g or 0)
        fat_value = float(log.fat_g or 0)

        st.html(
            f"""
            <div style="
                border:1px solid #e2e8f0;
                border-radius:18px;
                padding:1.1rem 1.2rem;
                margin:0.6rem 0;
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
                            font-size:1.05rem;
                            font-weight:700;
                            color:#0f4c5c;
                        ">
                            🍽️ {log.food_name}
                        </div>

                        <div style="
                            color:#64748b;
                            margin-top:0.25rem;
                            font-size:0.85rem;
                        ">
                            📅 {log.log_date}
                        </div>

                    </div>

                    <div style="
                        padding:0.35rem 0.7rem;
                        border-radius:999px;
                        background:#eff6ff;
                        color:#1d4ed8;
                        font-size:0.82rem;
                        font-weight:700;
                        white-space:nowrap;
                    ">
                        {calories_value:.0f} kcal
                    </div>

                </div>

                <div style="
                    display:flex;
                    flex-wrap:wrap;
                    gap:0.7rem;
                    margin-top:0.9rem;
                    padding-top:0.75rem;
                    border-top:1px solid #f1f5f9;
                    color:#64748b;
                    font-size:0.88rem;
                ">

                    <span>
                        🥩 Protein:
                        <strong style="color:#334155;">
                            {protein_value:.1f} g
                        </strong>
                    </span>

                    <span>
                        🍚 Carbs:
                        <strong style="color:#334155;">
                            {carbs_value:.1f} g
                        </strong>
                    </span>

                    <span>
                        🥑 Fat:
                        <strong style="color:#334155;">
                            {fat_value:.1f} g
                        </strong>
                    </span>

                    <span>
                        🔎 {log.source}
                    </span>

                </div>

            </div>
            """
        )

    # =========================================================
    # EDUCATIONAL DISCLAIMER
    # =========================================================

    st.divider()

    st.html(
        """
        <div style="
            margin-top:1.5rem;
            padding:1rem 1.2rem;
            border-radius:14px;
            border:1px solid #dbe3e8;
            background:#f8fafb;
            color:#64748b;
            font-size:0.82rem;
        ">

            🛡️ <strong>HealthGuard AI reminder:</strong>
            Nutrition information is intended for general educational
            tracking and may not reflect individual dietary needs.
            For personalized dietary advice, consult a qualified
            healthcare professional or registered dietitian.

        </div>
        """
    )