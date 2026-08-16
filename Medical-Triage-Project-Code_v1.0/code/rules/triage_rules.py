def evaluate_triage(state):
    """
    Deterministic triage baseline.

    This rule engine is the safety baseline.
    """

    symptoms = list(
        state.get("symptoms") or []
    )

    severity = state.get(
        "severity"
    )

    red_flags = []

    # =========================================================
    # High-Risk Red Flags
    # =========================================================

    if (
        "chest pain" in symptoms
        and "shortness of breath" in symptoms
    ):
        red_flags.append(
            "chest pain with shortness of breath"
        )

    if (
        "loss of consciousness"
        in symptoms
    ):
        red_flags.append(
            "loss of consciousness"
        )

    # =========================================================
    # HIGH
    # =========================================================

    if red_flags:

        return {
            "risk_level": "HIGH",
            "confidence": 0.85,
            "red_flags": red_flags,
            "recommendation": (
                "Emergency evaluation is required."
            ),
        }

    if severity == "severe":

        return {
            "risk_level": "HIGH",
            "confidence": 0.75,
            "red_flags": [],
            "recommendation": (
                "Prompt medical evaluation is recommended."
            ),
        }

    # =========================================================
    # LOW
    # =========================================================

    return {
        "risk_level": "LOW",
        "confidence": 0.60,
        "red_flags": [],
        "recommendation": (
            "Continue monitoring symptoms and seek "
            "medical advice if they worsen."
        ),
    }