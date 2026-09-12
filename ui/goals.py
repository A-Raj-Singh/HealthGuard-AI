import streamlit as st

from database.crud import (
    add_health_goal,
    list_health_goals,
    deactivate_health_goal,
    list_metrics,
)


def render(patient_id):
    st.title("🎯 Health Goals")

    st.caption(
        "Set simple wellness targets and track your progress over time."
    )

    # =========================================================
    # SET A GOAL
    # =========================================================

    st.subheader("Set a health goal")

    goal_options = {
        "Daily Steps": ("steps", "steps"),
        "Sleep": ("sleep_hours", "hours"),
        "Calories Burned": ("calories_burned", "kcal"),
        "Heart Rate": ("heart_rate", "bpm"),
    }

    selected_goal = st.selectbox(
        "Goal type",
        list(goal_options.keys()),
    )

    goal_type, unit = goal_options[selected_goal]

    target_value = st.number_input(
        f"Target ({unit})",
        min_value=1.0,
        value=5000.0,
        step=1.0,
    )

    if st.button("Set goal", use_container_width=True):
        add_health_goal(
            patient_id,
            goal_type,
            target_value,
            unit,
        )

        st.success(f"{selected_goal} goal created successfully.")
        st.rerun()

    st.divider()

    # =========================================================
    # ACTIVE GOALS
    # =========================================================

    st.subheader("Your active goals")

    goals = list_health_goals(patient_id, active_only=True)

    if not goals:
        st.info("You have not created any health goals yet.")
        return

    metrics = list_metrics(patient_id)

    latest_metric = metrics[-1] if metrics else None

    for goal in goals:
        st.markdown(f"### {goal.goal_type.replace('_', ' ').title()}")

        target = goal.target_value

        current_value = 0.0

        if latest_metric:
            current_value = getattr(
                latest_metric,
                goal.goal_type,
                0,
            ) or 0.0

        if goal.goal_type == "heart_rate":
            # For heart rate, show the latest recorded value
            progress = 0.0
        else:
            progress = min(current_value / target, 1.0) if target > 0 else 0.0

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Current",
                f"{current_value:g} {goal.unit}",
            )

        with col2:
            st.metric(
                "Target",
                f"{target:g} {goal.unit}",
            )

        if goal.goal_type != "heart_rate":
            st.progress(progress)

            percentage = min(
                (current_value / target) * 100,
                100,
            ) if target > 0 else 0

            st.caption(
                f"Progress: {percentage:.0f}%"
            )
        else:
            st.info(
                "Heart rate goals are displayed using your latest "
                "recorded heart-rate value."
            )

        if st.button(
            f"Remove {goal.goal_type.replace('_', ' ')} goal",
            key=f"remove_goal_{goal.id}",
        ):
            deactivate_health_goal(
                goal.id,
                patient_id,
            )
            st.rerun()

        st.divider()
