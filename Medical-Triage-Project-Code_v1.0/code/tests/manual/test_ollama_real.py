from application.config.llm_provider import build_llm
from application.config.settings import Settings


def main():
    settings = Settings()

    llm = build_llm(settings)

    response = llm.generate(
        "Explain what a headache is in one short sentence."
    )

    print("\nLLM RESPONSE:")
    print(response)


if __name__ == "__main__":
    main()