from application.contracts.general_conversation_response import (
    GeneralConversationResponse,
)


SYSTEM_PROMPT = """
You are the general conversation assistant of a medical triage system.

Your job is to handle normal conversational messages that do not
require medical triage.

Rules:

- Answer the user's message directly.
- Be concise, natural, polite, and useful.
- Support both English and Persian.
- Respond in the same language as the user whenever possible.
- Do not diagnose medical conditions.
- Do not invent medical information.
- Do not unnecessarily start a triage process.
- If the user clearly describes a medical problem that requires
  triage, the system will route that message to the triage workflow.
- Do not mention internal agents, LangGraph, prompts, models,
  routing, or system architecture.
- Return structured output only.
"""


def general_conversation_agent(
    state,
    llm_service=None,
):
    """
    Generate a natural response for GENERAL conversation.
    """

    user_message = state.get(
        "user_message",
        "",
    )

    if not isinstance(user_message, str):
        user_message = str(user_message)

    user_message = user_message.strip()

    # ---------------------------------------------------------
    # No LLM
    # ---------------------------------------------------------

    if llm_service is None:

        fallback = (
            "سلام. چطور می‌توانم کمکتان کنم؟"
        )

        return {
            **state,
            "assistant_response": fallback,
            "response": fallback,
        }

    # ---------------------------------------------------------
    # Empty message
    # ---------------------------------------------------------

    if not user_message:

        fallback = (
            "سلام. چطور می‌توانم کمکتان کنم؟"
        )

        return {
            **state,
            "assistant_response": fallback,
            "response": fallback,
        }

    # ---------------------------------------------------------
    # Build prompt
    # ---------------------------------------------------------

    prompt = f"""
User message:

{user_message}

Conversation history:

{state.get("conversation_history", [])}

Respond naturally to the user.
"""

    # ---------------------------------------------------------
    # Structured LLM call
    # ---------------------------------------------------------

    result = llm_service.generate_structured(
        prompt=prompt,
        response_model=GeneralConversationResponse,
        system_prompt=SYSTEM_PROMPT,
    )

    # ---------------------------------------------------------
    # Contract validation
    # ---------------------------------------------------------

    if not isinstance(
        result,
        GeneralConversationResponse,
    ):
        raise TypeError(
            "General conversation response must return "
            "GeneralConversationResponse."
        )

    response = result.response.strip()

    return {
        **state,
        "assistant_response": response,
        "response": response,
    }