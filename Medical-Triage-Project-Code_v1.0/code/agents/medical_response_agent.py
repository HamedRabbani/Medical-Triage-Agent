from application.services.llm_service import LLMService


SYSTEM_PROMPT = """
You are the response generation assistant of a medical triage system.

Generate the final patient-facing response using ONLY the
explicitly provided triage assessment.

Rules:
- Do not diagnose a disease.
- Do not invent symptoms, medical history, or test results.
- Do not change or override the deterministic triage risk level.
- Do not contradict the deterministic triage decision.
- Use retrieved medical knowledge only when it is relevant.
- For HIGH risk, clearly recommend prompt medical evaluation.
- For LOW risk, provide appropriate general guidance and
  explain when medical evaluation is needed.
- If red flags are present, mention them clearly.
- Keep the response concise, clear, and medically cautious.
- Respond in the same language as the user's message.

Supervisor rules:
- APPROVED means the assessment passed supervisor validation.
- REVIEW_REQUIRED means the deterministic rule and LLM assessment
  disagree or the case requires additional review.
- When status is REVIEW_REQUIRED, do not present the assessment
  as a definitive diagnosis.
- When status is REVIEW_REQUIRED and the deterministic risk is HIGH,
  preserve the HIGH risk recommendation.
- Never downgrade a deterministic HIGH risk because the LLM returned LOW.
"""


def medical_response_agent(
    state,
    llm_service=None,
):
    """
    Generate the final patient-facing triage response.

    This agent does not perform risk assessment.
    It converts the finalized triage state into
    a safe natural-language response.
    """

    if llm_service is None:
        return state

    user_message = state.get(
        "user_message",
        "",
    )

    if (
        not isinstance(user_message, str)
        or not user_message.strip()
    ):
        return {
            **state,
            "assistant_response": "",
            "response": "",
        }

    prompt = f"""
Patient message:
{user_message}

Triage assessment:

Risk level:
{state.get("risk_level")}

Confidence:
{state.get("confidence")}

Red flags:
{state.get("red_flags", [])}

Recommendation:
{state.get("recommendation")}

LLM risk level:
{state.get("llm_risk_level")}

LLM confidence:
{state.get("llm_confidence")}

Supervisor status:
{state.get("supervisor_status")}

Retrieved medical knowledge:
{state.get("rag_context", [])}

Generate the final patient-facing response.
"""

    response = llm_service.generate(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
    )

    return {
        **state,
        "assistant_response": response,
        "response": response,
    }