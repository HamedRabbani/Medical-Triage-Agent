from application.contracts.llm_risk_assessment import (
    LLMRiskAssessment,
)

from rules.triage_rules import evaluate_triage


SYSTEM_PROMPT = """
You are a medical triage risk assessment assistant.

Assess risk ONLY from explicitly provided patient information.

Return structured output.

risk_level must be exactly:
LOW
HIGH

Rules:
- Chest pain + shortness of breath -> HIGH
- Loss of consciousness -> HIGH
- Severe symptoms -> HIGH
- Otherwise -> LOW

Do not invent symptoms or medical information.
"""


def risk_agent(
    state,
    llm_service=None,
):
    """
    Perform deterministic and LLM-based risk assessment.

    The deterministic rule engine is the safety baseline.
    The LLM provides an independent assessment.

    Both results are preserved in the state.
    """

    # =========================================================
    # 1. Rule-based baseline
    # =========================================================

    rule_result = evaluate_triage(state)

    rule_risk_level = rule_result.get("risk_level")
    rule_confidence = rule_result.get("confidence")

    rule_red_flags = list(
        rule_result.get("red_flags") or []
    )

    rule_recommendation = rule_result.get(
        "recommendation"
    )

    # =========================================================
    # 2. Default LLM result
    # =========================================================

    llm_risk_level = None
    llm_confidence = None
    llm_red_flags = []
    llm_recommendation = None

    # =========================================================
    # 3. LLM assessment
    # =========================================================

    if llm_service is not None:

        prompt = f"""
Patient information:

Symptoms: {state.get("symptoms", [])}
Severity: {state.get("severity")}
Age: {state.get("age")}
Duration: {state.get("duration")}
Red flags: {state.get("red_flags", [])}

Assess the triage risk.
"""

        llm_result = llm_service.generate_structured(
            prompt=prompt,
            response_model=LLMRiskAssessment,
            system_prompt=SYSTEM_PROMPT,
        )

        # -----------------------------------------------------
        # Contract validation
        # -----------------------------------------------------

        if not isinstance(
            llm_result,
            LLMRiskAssessment,
        ):
            raise TypeError(
                "LLM risk assessment must return "
                "LLMRiskAssessment."
            )

        llm_risk_level = llm_result.risk_level
        llm_confidence = llm_result.confidence

        llm_red_flags = list(
            llm_result.red_flags or []
        )

        llm_recommendation = (
            llm_result.recommendation
        )

    # =========================================================
    # 4. Return complete state
    # =========================================================

    return {
        **state,

        # Rule Engine
        "risk_level": rule_risk_level,
        "confidence": rule_confidence,
        "red_flags": rule_red_flags,
        "recommendation": rule_recommendation,

        # LLM
        "llm_risk_level": llm_risk_level,
        "llm_confidence": llm_confidence,
        "llm_red_flags": llm_red_flags,
        "llm_recommendation": llm_recommendation,
    }