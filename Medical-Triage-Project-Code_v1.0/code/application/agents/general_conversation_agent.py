from application.contracts.general_chat_response import (
    GeneralChatResponse,
)


SYSTEM_PROMPT = """
You are the general conversation assistant of a medical triage system.

Your job is to handle casual and non-triage conversation.

Examples:
- greetings
- asking what the system can do
- asking how the system works
- casual conversation
- non-medical general questions

Important safety rules:
- Do not diagnose diseases.
- Do not make medical risk decisions.
- Do not determine triage severity.
- Do not override the triage workflow.
- If the user describes symptoms or asks for medical advice,
  provide a brief response indicating that the medical triage
  workflow should handle the request.
- Never claim to be a doctor.

Return a concise and natural response.
"""


def general_conversation_agent(
    state,
    llm_service,
):
    """
    Handle non-triage conversation.

    This agent must never modify medical triage state.
    """

    user_message = state.get("user_message", "")

    if not user_message:
        return {
            **state,
            "general_response": "",
        }

    prompt = f"""
User message:

{user_message}

Respond naturally as the general conversation assistant.
"""

    result = llm_service.generate_structured(
        prompt=prompt,
        response_model=GeneralChatResponse,
        system_prompt=SYSTEM_PROMPT,
    )

    return {
        **state,
        "general_response": result.response,
    }