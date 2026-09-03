"""
Local HealthGuard AI Assistant.

Works without OpenAI API credits.
Uses HealthGuard patient data and rule-based responses.
"""

from agents.tools import (
    get_patient_summary,
    get_medications,
    get_health_metrics,
)


def _summary(patient_id: int) -> str:
    try:
        result = get_patient_summary.invoke(
            {"patient_id": patient_id}
        )
        return str(result)

    except Exception as e:
        print("Summary error:", e)
        return "Unable to load your health summary."


def _medications(patient_id: int) -> str:
    try:
        result = get_medications.invoke(
            {"patient_id": patient_id}
        )

        return str(result)

    except Exception as e:
        print("Medication error:", e)
        return "Unable to load your medication information."


def _metrics(patient_id: int) -> str:
    try:
        result = get_health_metrics.invoke(
            {"patient_id": patient_id}
        )

        return str(result)

    except Exception as e:
        print("Metrics error:", e)
        return "Unable to load your health metrics."


def ask(prompt: str, patient_id: int) -> str:
    """
    Local HealthGuard chatbot.
    No OpenAI API required.
    """

    text = prompt.lower().strip()

    # Emergency safety response
    emergency_words = [
        "emergency",
        "can't breathe",
        "cannot breathe",
        "chest pain",
        "unconscious",
        "severe bleeding",
        "stroke",
        "suicide",
        "self harm",
        "self-harm",
    ]

    if any(word in text for word in emergency_words):
        return (
            "⚠️ This may require urgent medical attention.\n\n"
            "Please contact your local emergency service or seek "
            "immediate medical care.\n\n"
            "HealthGuard AI is an educational monitoring application "
            "and cannot diagnose or treat emergencies."
        )

    # Greeting
    if any(
        word in text
        for word in [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good evening",
        ]
    ):
        return (
            "Hello! 👋 I am your HealthGuard AI Assistant.\n\n"
            "I can help you review:\n"
            "• Health summary\n"
            "• Health metrics\n"
            "• Medications\n"
            "• Nutrition information\n\n"
            "Try asking: \"Show my health summary\""
        )

    # Medication
    if any(
        word in text
        for word in [
            "medication",
            "medicine",
            "medicines",
            "tablet",
            "tablets",
            "dose",
            "dosage",
        ]
    ):
        return _medications(patient_id)

    # Metrics
    if any(
        word in text
        for word in [
            "metric",
            "metrics",
            "steps",
            "sleep",
            "weight",
            "blood pressure",
            "pressure",
            "heart rate",
            "pulse",
            "calories burned",
        ]
    ):
        return _metrics(patient_id)

    # Health summary
    if any(
        word in text
        for word in [
            "health",
            "summary",
            "status",
            "overall",
            "profile",
            "dashboard",
        ]
    ):
        return (
            "📋 Here is your HealthGuard health summary:\n\n"
            + _summary(patient_id)
            + "\n\n"
            "This information is for monitoring and educational "
            "purposes only. It is not a medical diagnosis."
        )

    # Nutrition
    if any(
        word in text
        for word in [
            "food",
            "nutrition",
            "calorie",
            "calories",
            "protein",
            "carbohydrate",
            "carbs",
            "fat",
            "diet",
            "meal",
            "meals",
        ]
    ):
        return (
            "🥗 You can record and review nutrition information "
            "from the Nutrition page.\n\n"
            "Individual dietary needs vary. For personalized "
            "dietary advice, consult a qualified healthcare "
            "professional."
        )

    # Help
    if any(
        word in text
        for word in [
            "help",
            "what can you do",
            "features",
            "options",
        ]
    ):
        return (
            "🤖 I can help you review information stored in "
            "your HealthGuard profile.\n\n"
            "Try asking:\n"
            "• Show my health summary\n"
            "• What medications am I taking?\n"
            "• Show my health metrics\n"
            "• Tell me about nutrition\n"
            "• What can you do?\n\n"
            "I cannot diagnose medical conditions."
        )

    # Default
    return (
        "I can help you review your HealthGuard information.\n\n"
        "Try:\n"
        "• Show my health summary\n"
        "• What medications am I taking?\n"
        "• Show my health metrics\n"
        "• What can you do?\n\n"
        "This local assistant works without an OpenAI API."
    )