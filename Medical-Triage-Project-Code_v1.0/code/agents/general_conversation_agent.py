from application.contracts.general_conversation_response import (
    GeneralConversationResponse,
)


SYSTEM_PROMPT = """
You are the general conversation assistant of a medical triage system.

Your responsibility is to handle messages that do NOT require
medical triage of the user's current health situation.

Rules:
- Answer the user's message directly.
- Be concise and clear.
- Do not perform medical diagnosis.
- Do not invent medical information.
- If the user describes a current medical problem that requires
  triage, do not attempt to handle it as general conversation.
- Do not ask unnecessary questions.
- Return structured output only.
"""


def general_conversation_agent(
    state,
    llm_service=None,
):
    """
    Generate a response for GENERAL conversation.

    This agent must only be reached when the conversation
    intent has already been classified as GENERAL.
    """

    if llm_service is None:
        return {
            **state,
            "assistant_response": None,
        }

    user_message = state.get(
        "user_message",
        "",
    )

    if not isinstance(user_message, str):
        return {
            **state,
            "assistant_response": None,
        }

    user_message = user_message.strip()

    if not user_message:
        return {
            **state,
            "assistant_response": None,
        }

    prompt = f"""
User message:

{user_message}

Provide an appropriate general response.
"""

    result = llm_service.generate_structured(
        prompt=prompt,
        response_model=GeneralConversationResponse,
        system_prompt=SYSTEM_PROMPT,
    )

    if not isinstance(
        result,
        GeneralConversationResponse,
    ):
        return {
            **state,
            "assistant_response": None,
        }

    return {
        **state,
        "assistant_response": result.response,
    }