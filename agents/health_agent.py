"""
HealthGuard AI - LangChain Healthcare Agent

Uses:
- LangChain 1.x
- Google Gemini through langchain-google-genai
- HealthGuard patient-scoped healthcare tools

Safety:
- Emergency situations are detected before the LLM is called.
- The agent cannot choose another patient's ID.
- The agent does not diagnose or prescribe.
"""

from functools import lru_cache

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from agents.prompts import SYSTEM_PROMPT
from agents.tools import (
    get_health_metrics,
    get_medications,
    get_patient_summary,
)
from config import GEMINI_API_KEY, GEMINI_MODEL


# ---------------------------------------------------------------------
# Emergency safety detection
# ---------------------------------------------------------------------

EMERGENCY_PHRASES = (
    "emergency",
    "can't breathe",
    "cannot breathe",
    "difficulty breathing",
    "trouble breathing",
    "chest pain",
    "severe chest pain",
    "unconscious",
    "passed out",
    "severe bleeding",
    "stroke",
    "seizure",
    "suicide",
    "suicidal",
    "self harm",
    "self-harm",
)


def _is_emergency(text: str) -> bool:
    """Return True when the message contains an emergency phrase."""
    normalized = text.lower().strip()
    return any(phrase in normalized for phrase in EMERGENCY_PHRASES)


def _emergency_response() -> str:
    """Return a safe response for potentially urgent situations."""
    return (
        "⚠️ **This may require urgent medical attention.**\n\n"
        "Please contact your local emergency service or seek "
        "immediate medical care.\n\n"
        "HealthGuard AI cannot diagnose or treat emergencies."
    )


# ---------------------------------------------------------------------
# Patient-scoped tools
# ---------------------------------------------------------------------

def _build_patient_tools(patient_id: int):
    """
    Build tools that are permanently restricted to the logged-in patient.

    The LLM does not receive a patient_id argument, so it cannot request
    another patient's information.
    """

    @tool
    def patient_health_summary() -> str:
        """
        Retrieve the logged-in patient's stored health profile.

        Use this when the user asks about their personal health profile,
        age, basic health information, or wants a general health summary.
        """
        try:
            result = get_patient_summary.invoke(
                {"patient_id": patient_id}
            )
            return str(result)
        except Exception as exc:
            return (
                "Unable to retrieve the patient's health profile. "
                f"Internal error: {type(exc).__name__}"
            )

    @tool
    def patient_medications() -> str:
        """
        Retrieve the logged-in patient's current medications.

        Use this when the user asks what medications they take,
        their medication schedule, or medication-related stored data.
        """
        try:
            result = get_medications.invoke(
                {"patient_id": patient_id}
            )
            return str(result)
        except Exception as exc:
            return (
                "Unable to retrieve the patient's medication information. "
                f"Internal error: {type(exc).__name__}"
            )

    @tool
    def patient_health_metrics() -> str:
        """
        Retrieve the logged-in patient's recorded health metrics.

        Includes available information such as:
        - steps
        - calories burned
        - sleep hours
        - heart rate

        Use this when the user asks about their recorded health data,
        activity, sleep, heart rate, or trends.
        """
        try:
            result = get_health_metrics.invoke(
                {"patient_id": patient_id}
            )
            return str(result)
        except Exception as exc:
            return (
                "Unable to retrieve the patient's health metrics. "
                f"Internal error: {type(exc).__name__}"
            )

    return [
        patient_health_summary,
        patient_medications,
        patient_health_metrics,
    ]


# ---------------------------------------------------------------------
# LangChain agent
# ---------------------------------------------------------------------

@lru_cache(maxsize=32)
def _get_agent(patient_id: int):
    """Create and cache a patient-scoped LangChain agent."""

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    model = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GEMINI_API_KEY,
        temperature=0.2,
    )

    tools = _build_patient_tools(patient_id)

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent

# ---------------------------------------------------------------------
# Response extraction
# ---------------------------------------------------------------------

def _extract_response(result) -> str:
    """
    Extract the final assistant response from a LangChain agent result.
    """

    messages = result.get("messages", [])

    if not messages:
        return (
            "I wasn't able to generate a response. "
            "Please try again."
        )

    # Search backwards for the last message containing content.
    for message in reversed(messages):
        content = getattr(message, "content", "")

        if isinstance(content, str):
            content = content.strip()

            if content:
                return content

        elif isinstance(content, list):
            parts = []

            for item in content:
                if isinstance(item, dict):
                    text = item.get("text")

                    if text:
                        parts.append(str(text))

                elif isinstance(item, str):
                    parts.append(item)

            response = "\n".join(parts).strip()

            if response:
                return response

    return (
        "I wasn't able to generate a response. "
        "Please try asking your question again."
    )


# ---------------------------------------------------------------------
# Public AI function
# ---------------------------------------------------------------------

def ask(prompt: str, patient_id: int) -> str:
    """
    Send a user question to the HealthGuard AI agent.

    Parameters
    ----------
    prompt:
        User's question.

    patient_id:
        ID of the currently logged-in patient.

    Returns
    -------
    str
        AI-generated response.
    """

    # Validate input.
    if not isinstance(prompt, str):
        return "Please enter a valid health question."

    prompt = prompt.strip()

    if not prompt:
        return (
            "Please enter a health question or choose one "
            "of the suggested questions."
        )

    # Validate patient context.
    if not patient_id:
        return (
            "⚠️ Your account is not linked to a patient profile."
        )

    # Emergency protection happens before the LLM.
    if _is_emergency(prompt):
        return _emergency_response()

    # Check configuration before creating the agent.
    if not GEMINI_API_KEY:
        return (
            "⚠️ **The AI assistant is not configured.**\n\n"
            "Please configure `GEMINI_API_KEY` in your local "
            "`.env` file or Streamlit Cloud Secrets."
        )

    try:
        agent = _get_agent(int(patient_id))

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            }
        )

        answer = _extract_response(result)

        if not answer:
            return (
                "I wasn't able to generate a response. "
                "Please try asking your question again."
            )

        return answer

    except Exception as exc:
        # Print the complete technical error in the Streamlit terminal.
        # This is useful for debugging without exposing it to the user.
        import traceback

        print("\n" + "=" * 70)
        print("HEALTHGUARD AI AGENT ERROR")
        print("=" * 70)
        print(f"Error type: {type(exc).__name__}")
        print(f"Error: {exc}")
        traceback.print_exc()
        print("=" * 70 + "\n")

        # Give the user a clean message.
        return (
            "⚠️ **I couldn't connect to the AI service right now.**\n\n"
            "Please try again in a moment.\n\n"
            "You can still use the Medication, Nutrition, "
            "Medical Information, Dashboard and Reports sections.\n\n"
            "If the problem continues, check the Streamlit terminal "
            "for the AI service error."
        )
