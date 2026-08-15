from application.config.llm_provider import build_llm
from application.config.settings import Settings
from application.contracts.llm_test_response import LLMTestResponse

from tests.evaluation.llm_baseline_cases import CASES


def main():
    llm = build_llm(Settings())

    passed = 0

    for case in CASES:

        user_input = case["input"]

        prompt = (
            "You are a medical symptom extraction system.\n"
            "Your task is ONLY to extract symptoms explicitly mentioned by the user.\n\n"

            "Rules:\n"
            "1. Extract every explicitly mentioned symptom.\n"
            "2. Do NOT infer or guess symptoms.\n"
            "3. Do NOT add symptoms that are not explicitly mentioned.\n"
            "4. Translate Persian symptoms into standard English medical names.\n"
            "5. Preserve English symptoms as standard English medical names.\n"
            "6. Return an empty list if no specific symptom is mentioned.\n"
            "7. Return ONLY data that matches the requested structured schema.\n\n"

            "Examples:\n"
            "من سردرد دارم -> headache\n"
            "من تب دارم -> fever\n"
            "من سرفه می‌کنم -> cough\n"
            "من تهوع دارم -> nausea\n"
            "قفسه سینه‌ام درد می‌کند -> chest pain\n"
            "حالم خوب نیست -> empty list\n"
            "I have fever and a cough -> fever, cough\n\n"

            f"User input:\n{user_input}"
        )

        result = llm.generate_structured(
            prompt=prompt,
            response_model=LLMTestResponse,
        )

        expected = sorted(case["expected_symptoms"])
        actual = sorted(
            symptom.lower()
            for symptom in result.symptoms
        )

        success = actual == expected

        print(f"\nInput: {user_input}")
        print(f"Expected: {expected}")
        print(f"Actual: {actual}")
        print(f"PASS: {success}")

        if success:
            passed += 1

    print(f"\nScore: {passed}/{len(CASES)}")


if __name__ == "__main__":
    main()