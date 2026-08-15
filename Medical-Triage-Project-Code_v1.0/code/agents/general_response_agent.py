SYSTEM_PROMPT = """
You are the general conversation assistant of a medical triage system.

Respond naturally to the user's message.

Rules:
- Do not diagnose.
- Do not invent medical facts.
- If the user is clearly asking for medical triage,
  do not handle the case here.
- Keep the response relevant to the user's message.
- Do not use predefined question-answer patterns.
"""


def general_response_agent(
    state,
    llm_service=None,
):
    if llm_service is None:
        return state

    text = state.get("user_message", "")

    if not isinstance(text, str) or not text.strip():
        return {
            **state,
            "response": "",
        }

    response = llm_service.generate(
        prompt=text,
        system_prompt=SYSTEM_PROMPT,
    )

    return {
        **state,
        "response": response,
    }