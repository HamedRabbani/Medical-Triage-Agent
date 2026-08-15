from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.conversation_intent import (
    ConversationIntent,
)
from application.contracts.general_conversation_response import (
    GeneralConversationResponse,
)


SYSTEM_PROMPT = """
You are the conversation understanding layer of a medical triage system.

Classify the user's message into exactly one intent:

TRIAGE:
The user is providing, describing, discussing, or asking about
their own symptoms, medical condition, injury, or health situation
that may require triage.

GENERAL:
The user is having a general conversation or asking something
that does not require medical triage of their current situation.

Rules:
- Understand meaning and context.
- Do not use keyword matching.
- Do not diagnose.
- Do not invent information.
- Return structured output only.
"""


EXTRACTION_SYSTEM_PROMPT = """
You are the medical information extraction layer of a medical
triage system.

Extract ONLY information explicitly provided by the user.

Extract:
- symptoms
- severity
- age
- duration
- red flags

Rules:
- Do not invent information.
- Do not diagnose.
- Do not infer unstated symptoms.
- Preserve previously known information.
- Return structured output only.
"""


GENERAL_RESPONSE_SYSTEM_PROMPT = """
You are the general conversation response layer of a medical
triage system.

Respond naturally and briefly to the user's message.

Rules:
- Do not perform medical triage.
- Do not diagnose.
- Do not invent medical information.
- Return structured output only.
"""


def conversation_agent(
    state,
    llm_service=None,
):
    """
    Conversation understanding layer.

    GENERAL:

        User Message
             ↓
        Intent Classification
             ↓
        General Response
             ↓
            END

    TRIAGE:

        User Message
             ↓
        Intent Classification
             ↓
        Medical Extraction
             ↓
        Triage Pipeline
    """

    # =========================================================
    # No LLM
    # =========================================================

    if llm_service is None:
        return state

    text = state.get(
        "user_message",
        "",
    )

    # =========================================================
    # Empty Message
    # =========================================================

    if not isinstance(text, str) or not text.strip():

        response = "Hello. How can I help you?"

        return {
            **state,
            "intent": "GENERAL",
            "intent_confidence": 1.0,
            "assistant_response": response,
            "response": response,
        }

    # =========================================================
    # 1. Intent Classification
    # =========================================================

    intent_result = llm_service.generate_structured(
        prompt=f"""
User message:

{text}

Classify the intent of this message.
""",
        response_model=ConversationIntent,
        system_prompt=SYSTEM_PROMPT,
    )

    # Defensive validation
    if not isinstance(
        intent_result,
        ConversationIntent,
    ):
        return state

    result = {
        **state,
        "intent": intent_result.intent,
        "intent_confidence": intent_result.confidence,
    }

    # =========================================================
    # 2. GENERAL Conversation
    # =========================================================

    if intent_result.intent == "GENERAL":

        response_result = (
            llm_service.generate_structured(
                prompt=f"""
User message:

{text}

Generate a natural response to this message.
""",
                response_model=GeneralConversationResponse,
                system_prompt=GENERAL_RESPONSE_SYSTEM_PROMPT,
            )
        )

        # Defensive validation
        if not isinstance(
            response_result,
            GeneralConversationResponse,
        ):
            return {
                **result,
                "assistant_response": (
                    "Hello. How can I help you?"
                ),
                "response": (
                    "Hello. How can I help you?"
                ),
            }

        response = response_result.response

        return {
            **result,
            "assistant_response": response,
            "response": response,
        }

    # =========================================================
    # 3. TRIAGE Medical Extraction
    # =========================================================

    prompt = f"""
Previous known information:

Symptoms: {state.get("symptoms", [])}
Severity: {state.get("severity")}
Age: {state.get("age")}
Duration: {state.get("duration")}
Red flags: {state.get("red_flags", [])}

New patient message:

{text}

Extract only NEW medical information explicitly provided
in the new message.
"""

    extraction_result = llm_service.generate_structured(
        prompt=prompt,
        response_model=ConversationExtraction,
        system_prompt=EXTRACTION_SYSTEM_PROMPT,
    )

    # Defensive validation
    if not isinstance(
        extraction_result,
        ConversationExtraction,
    ):
        return result

    # =========================================================
    # 4. Merge Symptoms
    # =========================================================

    symptoms = list(
        state.get("symptoms") or []
    )

    for symptom in (
        extraction_result.symptoms or []
    ):
        if symptom not in symptoms:
            symptoms.append(symptom)

    # =========================================================
    # 5. Merge Red Flags
    # =========================================================

    red_flags = list(
        state.get("red_flags") or []
    )

    for flag in (
        extraction_result.red_flags or []
    ):
        if flag not in red_flags:
            red_flags.append(flag)

    # =========================================================
    # 6. Return TRIAGE State
    # =========================================================

    return {
        **result,

        "symptoms": symptoms,

        "severity": (
            extraction_result.severity
            if extraction_result.severity is not None
            else state.get("severity")
        ),

        "age": (
            extraction_result.age
            if extraction_result.age is not None
            else state.get("age")
        ),

        "duration": (
            extraction_result.duration
            if extraction_result.duration is not None
            else state.get("duration")
        ),

        "red_flags": red_flags,
    }