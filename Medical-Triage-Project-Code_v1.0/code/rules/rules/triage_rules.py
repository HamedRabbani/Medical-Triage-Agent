def evaluate_triage(state):

    symptoms = state.get("symptoms", [])
    severity = state.get("severity")

    red_flags = []

    if (
        "chest pain" in symptoms
        and "shortness of breath" in symptoms
    ):
        red_flags.append(
            "chest pain with shortness of breath"
        )

    if "loss of consciousness" in symptoms:
        red_flags.append(
            "loss of consciousness"
        )

    if red_flags:

        return {
            "risk_level": "HIGH",
            "confidence": 0.85,
            "red_flags": red_flags,
            "recommendation":
                "Emergency evaluation is required."
        }

    if severity == "severe":

        return {
            "risk_level": "HIGH",
            "confidence": 0.75,
            "red_flags": [],
            "recommendation":
                "Prompt medical evaluation is recommended."
        }

    return {
        "risk_level": "LOW",
        "confidence": 0.60,
        "red_flags": [],
        "recommendation":
            "Continue monitoring symptoms and seek medical advice if they worsen."
    }