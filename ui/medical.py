import streamlit as st

from api.medical_api import search_medical_info
from config import MEDICAL_DISCLAIMER


NLM_SOURCE_NAME = "U.S. National Library of Medicine (NLM)"


def render():
    # =========================================================
    # HEADER
    # =========================================================

    st.title("🩺 Medical Information")

    st.caption(
        "Explore general health information from trusted medical resources."
    )

    # =========================================================
    # INTRO CARD
    # =========================================================

    st.html(
        """
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
                    width:54px;
                    height:54px;
                    border-radius:16px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:white;
                    font-size:1.8rem;
                    box-shadow:0 3px 10px rgba(15,76,92,0.08);
                ">
                    🩺
                </div>

                <div>
                    <div style="
                        font-size:1.15rem;
                        font-weight:750;
                        color:#0f4c5c;
                    ">
                        Learn about health topics
                    </div>

                    <div style="
                        margin-top:0.25rem;
                        color:#64748b;
                        font-size:0.9rem;
                    ">
                        Search for general information about conditions,
                        symptoms, wellness topics, and more.
                    </div>
                </div>
            </div>
        </div>
        """
    )

    # =========================================================
    # SEARCH
    # =========================================================

    st.subheader("🔎 Search medical information")

    with st.form("medical_search_form"):
        query = st.text_input(
            "Health topic",
            placeholder="e.g. hypertension, asthma, diabetes",
        )

        search_button = st.form_submit_button(
            "🔎 Search",
            type="primary",
            width="stretch",
        )

    # =========================================================
    # SEARCH RESULTS
    # =========================================================

    if search_button:
        if not query.strip():
            st.warning("Please enter a health topic to search.")

        else:
            search_query = query.strip()

            with st.spinner(
                "🔎 Searching trusted medical information..."
            ):
                try:
                    results = search_medical_info(search_query)

                except Exception:
                    results = []

                    st.error(
                        "The medical information service is temporarily "
                        "unavailable. Please try again later."
                    )

            if results:
                st.success(
                    f"✅ Found {len(results)} result(s) for "
                    f"**{search_query}**."
                )

                st.subheader("📚 Search results")

                for item in results:
                    title = item.get("title") or "Health topic"

                    summary = (
                        item.get("summary")
                        or "No summary is available for this result."
                    )

                    url = item.get("url")

                    with st.container(border=True):
                        st.markdown(f"### 🩺 {title}")

                        st.write(summary)

                        st.caption(
                            f"Source: {NLM_SOURCE_NAME}"
                        )

                        if url:
                            st.link_button(
                                "🔗 Open NLM source",
                                url,
                            )

            else:
                st.warning(
                    "No results found or the medical information "
                    "service is temporarily unavailable."
                )

    # =========================================================
    # QUICK TOPICS
    # =========================================================

    st.divider()

    st.subheader("💡 Popular topics")

    topic1, topic2, topic3, topic4 = st.columns(4)

    selected_topic = None

    with topic1:
        if st.button(
            "❤️ Heart health",
            width="stretch",
        ):
            selected_topic = "heart health"

    with topic2:
        if st.button(
            "🫁 Asthma",
            width="stretch",
        ):
            selected_topic = "asthma"

    with topic3:
        if st.button(
            "🩸 Diabetes",
            width="stretch",
        ):
            selected_topic = "diabetes"

    with topic4:
        if st.button(
            "🧠 Mental wellness",
            width="stretch",
        ):
            selected_topic = "mental health"

    if selected_topic:
        with st.spinner(
            f"🔎 Searching for {selected_topic}..."
        ):
            try:
                results = search_medical_info(selected_topic)

            except Exception:
                results = []

                st.error(
                    "The medical information service is temporarily "
                    "unavailable. Please try again later."
                )

        if results:
            st.subheader(
                f"📚 Results for {selected_topic.title()}"
            )

            for item in results:
                title = item.get("title") or "Health topic"

                summary = (
                    item.get("summary")
                    or "No summary is available for this result."
                )

                url = item.get("url")

                with st.container(border=True):
                    st.markdown(f"### 🩺 {title}")

                    st.write(summary)

                    st.caption(
                        f"Source: {NLM_SOURCE_NAME}"
                    )

                    if url:
                        st.link_button(
                            "🔗 Open NLM source",
                            url,
                        )

        else:
            st.warning(
                "No information was found for this topic."
            )

    # =========================================================
    # DISCLAIMER
    # =========================================================

    st.divider()

    st.warning(MEDICAL_DISCLAIMER)

    st.html(
        """
        <div style="
            margin-top:0.8rem;
            padding:1rem 1.2rem;
            border-radius:14px;
            border:1px solid #dbe3e8;
            background:#f8fafb;
            color:#64748b;
            font-size:0.82rem;
        ">
            🛡️ <strong>HealthGuard AI reminder:</strong>
            Medical information provided here is intended for general
            educational purposes. It should not be used for diagnosis,
            treatment, or emergency medical decisions.
        </div>
        """
    )