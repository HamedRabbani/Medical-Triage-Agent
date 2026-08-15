from application.config.llm_provider import build_llm
from application.config.settings import Settings
from application.contracts.llm_risk_assessment import LLMRiskAssessment


CASES = [
    {
        "input": "I have chest pain and shortness of breath.",
        "expected_risk": "HIGH",
        "expected_red_flags": [
            "chest pain with shortness of breath"
        ],
    },
    {
        "input": "I lost consciousness.",
        "expected_risk": "HIGH",
        "expected_red_flags": [
            "loss of consciousness"
        ],
    },
    {
        "input": "I have severe headache.",
        "expected_risk": "HIGH",
        "expected_red_flags": [],
    },
    {
        "input": "I have a mild headache.",
        "expected_risk": "LOW",
        "expected_red_flags": [],
    },
]


SYSTEM_PROMPT = """
You are a medical triage risk assessment assistant.

Your task is to assess the risk level based ONLY on the information
explicitly provided by the patient.

Return a structured response.

Rules:

1. risk_level must be exactly one of:
   LOW
   HIGH

2. confidence must be a number between 0 and 1.

3. red_flags must contain only explicitly supported dangerous findings.

4. Use these rules:

- Chest pain + shortness of breath -> HIGH
  red_flag:
  "chest pain with shortness of breath"

- Loss of consciousness -> HIGH
  red_flag:
  "loss of consciousness"

- Severe symptoms -> HIGH

- Otherwise -> LOW

5. Do not invent symptoms.
6. Do not add information that is not present.
7. recommendation must be appropriate for the risk level.
"""


def main():
    llm = build_llm(Settings())

    passed = 0

    for case in CASES:

        result = llm.generate_structured(
            prompt=f"""
Patient input:

{case["input"]}

Assess the triage risk.
""",
            response_model=LLMRiskAssessment,
            system_prompt=SYSTEM_PROMPT,
        )

        risk_pass = (
            result.risk_level == case["expected_risk"]
        )

        red_flags_pass = all(
            flag in result.red_flags
            for flag in case["expected_red_flags"]
        )

        case_pass = risk_pass and red_flags_pass

        if case_pass:
            passed += 1

        print()
        print("Input:", case["input"])
        print("Expected Risk:", case["expected_risk"])
        print("Actual Risk:", result.risk_level)
        print("Expected Red Flags:", case["expected_red_flags"])
        print("Actual Red Flags:", result.red_flags)
        print("Confidence:", result.confidence)
        print("PASS:", case_pass)

    print()
    print(f"Score: {passed}/{len(CASES)}")


if __name__ == "__main__":
    main()