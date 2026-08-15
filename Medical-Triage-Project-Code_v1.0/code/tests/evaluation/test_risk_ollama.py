from agents.risk_agent import risk_agent

from tests.evaluation.risk_baseline_cases import (
    RISK_BASELINE_CASES,
)


def main():

    total = len(RISK_BASELINE_CASES)
    agreements = 0
    false_negatives = 0
    false_positives = 0

    print("\n=== RISK AGENT EVALUATION ===\n")

    for case in RISK_BASELINE_CASES:

        state = case["state"]
        expected = case["expected_risk"]

        result = risk_agent(state)

        rule_result = result["risk_level"]
        llm_result = result["llm_risk_level"]

        rule_match = rule_result == expected
        llm_match = llm_result == expected

        if llm_match:
            agreements += 1

        if expected == "HIGH" and llm_result == "LOW":
            false_negatives += 1

        if expected == "LOW" and llm_result == "HIGH":
            false_positives += 1

        print(f"Case: {case['name']}")
        print(f"Expected: {expected}")
        print(f"Rule:     {rule_result}")
        print(f"LLM:      {llm_result}")
        print(f"Rule OK:  {rule_match}")
        print(f"LLM OK:   {llm_match}")
        print("-" * 40)

    agreement_rate = agreements / total

    print("\n=== SUMMARY ===")
    print(f"Total cases:       {total}")
    print(f"LLM agreements:    {agreements}")
    print(f"Agreement rate:    {agreement_rate:.2%}")
    print(f"False negatives:   {false_negatives}")
    print(f"False positives:   {false_positives}")


if __name__ == "__main__":
    main()