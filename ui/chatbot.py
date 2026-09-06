import streamlit as st

from agents.health_agent import ask


def render(patient_id: int):
    st.markdown(
        """
        <style>
        .block-container {
            padding-bottom: 8rem !important;
        }

        [data-testid="stChatInput"] {
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================
    # HEADER
    # =========================================================

    st.title("🤖 HealthGuard AI Assistant")

    st.caption(
        "Your intelligent health companion for reviewing your recorded "
        "health information and understanding your daily patterns."
    )

    # =========================================================
    # AI INTRO CARD
    # =========================================================

    st.html(
        """
        <div style="
            padding:1.25rem 1.4rem;
            border-radius:20px;
            background:linear-gradient(
                135deg,
                rgba(15,76,92,0.08),
                rgba(59,130,246,0.06)
            );
            border:1px solid rgba(15,76,92,0.12);
            margin:0.8rem 0 1.2rem 0;
        ">

            <div style="
                display:flex;
                align-items:center;
                gap:1rem;
            ">

                <div style="
                    width:52px;
                    height:52px;
                    border-radius:16px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:white;
                    font-size:1.8rem;
                    box-shadow:0 3px 10px rgba(15,76,92,0.08);
                ">
                    🤖
                </div>

                <div>

                    <div style="
                        font-size:1.15rem;
                        font-weight:750;
                        color:#0f4c5c;
                    ">
                        Hello! I'm your HealthGuard AI assistant.
                    </div>

                    <div style="
                        margin-top:0.25rem;
                        color:#64748b;
                        font-size:0.9rem;
                    ">
                        Ask me about your health metrics, medications,
                        nutrition, or recorded health information.
                    </div>

                </div>

            </div>

        </div>
        """
    )

    # =========================================================
    # SAFETY INFORMATION
    # =========================================================

    st.info(
        "🛡️ HealthGuard AI provides educational information and helps "
        "you review information recorded in your profile. It is not a "
        "substitute for a qualified healthcare professional."
    )

    # =========================================================
    # SESSION STATE
    # =========================================================

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # =========================================================
    # SUGGESTED QUESTIONS
    # =========================================================

    st.subheader("💡 Try asking")

    q1, q2, q3 = st.columns(3)

    suggestion = None

    with q1:
        if st.button(
            "📊 Review my health",
            width="stretch",
        ):
            suggestion = "Can you review my recorded health information?"

    with q2:
        if st.button(
            "💊 Check my medications",
            width="stretch",
        ):
            suggestion = "Can you summarize my recorded medications?"

    with q3:
        if st.button(
            "🥗 Review my nutrition",
            width="stretch",
        ):
            suggestion = "Can you summarize my recent nutrition information?"

    st.write("")

    # =========================================================
    # CHAT HISTORY
    # =========================================================

    if st.session_state.chat_messages:

        st.subheader("💬 Conversation")

        for message in st.session_state.chat_messages:

            with st.chat_message(
                message["role"]
            ):
                st.markdown(
                    message["content"]
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
                margin:0.8rem 0 1rem 0;
            ">

                <div style="
                    font-size:2.7rem;
                    margin-bottom:0.5rem;
                ">
                    💬
                </div>

                <div style="
                    font-size:1.15rem;
                    font-weight:700;
                    color:#0f4c5c;
                ">
                    Start a conversation
                </div>

                <div style="
                    color:#64748b;
                    margin-top:0.4rem;
                    font-size:0.9rem;
                ">
                    Ask a question or choose one of the suggested
                    topics above.
                </div>

            </div>
            """
        )

    # =========================================================
    # CHAT INPUT
    # =========================================================

    prompt = st.chat_input(
        "Ask about your health metrics, medications, nutrition, or dashboard..."
    )

    # Use a suggested question if one was clicked.
    if suggestion:
        prompt = suggestion

    # =========================================================
    # PROCESS MESSAGE
    # =========================================================

    if prompt:

        # Add user message
        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Ask AI
        with st.chat_message("assistant"):

            with st.spinner(
                "🧠 Checking your HealthGuard information..."
            ):

                try:

                    answer = ask(
                        prompt,
                        patient_id,
                    )

                except Exception:

                    answer = (
                        "⚠️ The AI assistant is temporarily unavailable. "
                        "You can continue using the other HealthGuard AI "
                        "features."
                    )

            st.markdown(answer)

        # Save assistant response
        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    # =========================================================
    # CHAT CONTROLS
    # =========================================================

    if st.session_state.chat_messages:

        st.divider()

        control1, control2 = st.columns(
            [1, 4]
        )

        with control1:

            if st.button(
                "🗑️ Clear chat",
                width="stretch",
            ):

                st.session_state.chat_messages = []

                st.rerun()

        with control2:

            st.caption(
                "💡 Your conversation is maintained during this session."
            )

    # =========================================================
    # FOOTER
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

            🛡️ <strong>HealthGuard AI safety reminder:</strong>
            AI-generated information is for educational and monitoring
            purposes. For urgent symptoms, diagnosis, treatment decisions,
            or personalized medical advice, consult an appropriate
            healthcare professional.

        </div>
        """
    )