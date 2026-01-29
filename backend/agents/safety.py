def safety_check_study_only(user_text: str) -> bool:
    """
    Simple safety gate:
    - If user asks patient-specific or personal medical advice, block.
    This app is for study purposes only.
    """
    t = (user_text or "").lower()

    high_risk_markers = [
        "i have", "my symptoms", "my chest", "my blood", "my bp", "my ecg",
        "should i take", "what should i do", "emergency", "urgent",
        "my patient", "treat me", "diagnose me", "prescribe"
    ]
    return not any(m in t for m in high_risk_markers)

STUDY_ONLY_MESSAGE = (
    "I can’t help with personal/patient-specific medical advice. "
    "I can help you study medical concepts from your uploaded notes. "
    "Try asking: “Explain ___” or “Quiz me on ___ using my notes.”"
)
