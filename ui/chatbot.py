import streamlit as st

from agents.health_agent import ask


def render(patient_id: int):
    st.title("🤖 HealthGuard AI Assistant")

    st.info(
        "HealthGuard AI provides educational health information and helps "
        "you review information recorded in your profile. It is not a "
        "substitute for a qualified healthcare professional."
    )

    st.subheader("Ask your health assistant")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask about your health metrics, medications, nutrition, or dashboard..."
    )

    if prompt:
        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Checking your HealthGuard information..."):
                try:
                    answer = ask(prompt, patient_id)
                except Exception:
                    answer = (
                        "⚠️ The AI assistant is temporarily unavailable. "
                        "You can continue using the other HealthGuard AI "
                        "features."
                    )

                st.markdown(answer)

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    if st.session_state.chat_messages:
        if st.button("Clear chat"):
            st.session_state.chat_messages = []
            st.rerun()