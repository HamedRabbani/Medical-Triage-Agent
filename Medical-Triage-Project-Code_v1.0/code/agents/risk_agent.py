from rules.triage_rules import evaluate_triage


def risk_agent(state):

    result = evaluate_triage(state)

    return {
        **state,
        "risk_level": result["risk_level"],
        "confidence": result["confidence"],
        "red_flags": result["red_flags"],
        "recommendation": result["recommendation"],
    }