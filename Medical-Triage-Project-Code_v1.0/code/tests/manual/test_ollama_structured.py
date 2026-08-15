from application.config.llm_provider import build_llm
from application.config.settings import Settings
from application.contracts.llm_test_response import LLMTestResponse


def main():
    settings = Settings()
    llm = build_llm(settings)

    result = llm.generate_structured(
    prompt=(
        "Extract the symptoms from this text.\n"
        "The text says: من سردرد و تب دارم\n"
        "Return both symptoms in the symptoms list."
    ),
    response_model=LLMTestResponse,
)

    print("\nSTRUCTURED RESPONSE:")
    print(result)
    print("\nType:", type(result))
    print("Symptoms:", result.symptoms)
    print("Confidence:", result.confidence)


if __name__ == "__main__":
    main()



# python -m tests.manual.test_ollama_real
# python tests/manual/test_ollama_structured.py
