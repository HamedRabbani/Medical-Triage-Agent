from application.contracts.general_conversation_response import (
    GeneralConversationResponse,
)


SYSTEM_PROMPT = """
You are the general conversation assistant of a medical AI triage system.

Rules:
- Always answer in the same language as the user.
- If the user writes Persian, answer only in Persian.
- If the user writes English, answer only in English.
- Be natural and concise.
- Do not diagnose diseases.
- Do not make medical decisions.
- Do not mention system architecture.
- Return only the final answer.
"""


def general_conversation_agent(
    state,
    llm_service=None,
):
    """
    Handle GENERAL conversation.
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


    print(
        "\n========== GENERAL DEBUG =========="
    )

    print(
        "USER MESSAGE:",
        user_message,
    )

    print(
        "LLM SERVICE:",
        llm_service,
    )


    # Empty message

    if not user_message:

        response = (
            "سلام. چطور می‌توانم کمکتان کنم؟"
        )

        print(
            "EMPTY FALLBACK:",
            response,
        )

        return {
            **state,
            "assistant_response": response,
            "response": response,
        }


    # No LLM available

    if llm_service is None:

        response = (
            "سلام. چطور می‌توانم کمکتان کنم؟"
        )

        print(
            "NO LLM FALLBACK:",
            response,
        )

        return {
            **state,
            "assistant_response": response,
            "response": response,
        }


    # Prompt

    prompt = f"""
User message:

{user_message}

Reply naturally.
"""


    try:

        response = llm_service.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
        )


        print(
            "RAW LLM RESPONSE:",
            response,
        )


        if not isinstance(
            response,
            str,
        ):

            response = str(response)


        response = response.strip()


    except Exception as exc:

        print(
            "GENERAL LLM ERROR:",
            exc,
        )

        response = (
            "متوجه شدم. چطور می‌توانم کمکتان کنم؟"
        )


    if not response:

        response = (
            "متوجه شدم. چطور می‌توانم کمکتان کنم؟"
        )


    print(
        "FINAL RESPONSE:",
        response,
    )

    print(
        "===================================\n"
    )


    return {
        **state,
        "assistant_response": response,
        "response": response,
    }