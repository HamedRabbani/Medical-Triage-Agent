SYSTEM_PROMPT = """
You are a general conversation assistant.

Reply naturally, briefly, and in the same language as the user.

Rules:
- Do not diagnose diseases.
- Do not make medical risk decisions.
- If the user reports symptoms or asks for medical advice,
  the medical triage workflow should handle the request.
- Never claim to be a doctor.
"""


def general_conversation_agent(
    state,
    llm_service=None,
):
    """
    Handle GENERAL conversation.

    General conversation uses plain-text generation.
    Structured output is reserved for machine-readable
    medical extraction and risk assessment.
    """

    user_message = state.get(
        "user_message",
        "",
    )

    if not isinstance(
        user_message,
        str,
    ):
        user_message = str(user_message)

    user_message = user_message.strip()

    # =========================================================
    # Authorization context
    # =========================================================

    roles = [
        str(role).lower()
        for role in state.get(
            "user_roles",
            [],
        )
    ]

    patient_id = state.get(
        "patient_id"
    )

    # =========================================================
    # Medical request without patient context
    # =========================================================

    medical_keywords = [
        "درد",
        "تب",
        "سردرد",
        "قفسه سینه",
        "علائم",
        "بیماری",
        "pain",
        "fever",
        "symptom",
        "chest pain",
    ]

    if (
        "patient" not in roles
        and patient_id is None
        and any(
            keyword in user_message.lower()
            for keyword in medical_keywords
        )
    ):
        response = (
            "برای انجام ارزیابی پزشکی، "
            "لطفاً با حساب بیمار وارد شوید "
            "یا ابتدا یک بیمار را انتخاب کنید."
        )

        return {
            **state,
            "assistant_response": response,
            "response": response,
        }

    # =========================================================
    # No LLM
    # =========================================================

    if llm_service is None:
        response = (
            "سلام. چطور می‌توانم کمکتان کنم؟"
        )

        return {
            **state,
            "assistant_response": response,
            "response": response,
        }

    # =========================================================
    # Empty message
    # =========================================================

    if not user_message:
        response = (
            "سلام. چطور می‌توانم کمکتان کنم؟"
        )

        return {
            **state,
            "assistant_response": response,
            "response": response,
        }

    # =========================================================
    # Plain prompt
    # =========================================================

    prompt = user_message

    # =========================================================
    # Plain-text generation
    # =========================================================

    response = llm_service.generate(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
    )

    if not isinstance(
        response,
        str,
    ):
        raise TypeError(
            "General conversation response must be a string."
        )

    response = response.strip()

    if not response:
        response = (
            "متوجه شدم. چطور می‌توانم کمکتان کنم؟"
        )

    return {
        **state,
        "assistant_response": response,
        "response": response,
    }