from application.config.llm_provider import build_llm
from application.config.settings import Settings
from application.services.llm_service import LLMService

from agents.symptom_agent import symptom_agent


def main():

    llm = build_llm(Settings())
    llm_service = LLMService(llm)

    state = {
        "user_message": "من تب و سردرد دارم",
        "conversation_history": [],
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
    }

    result = symptom_agent(
        state,
        llm_service=llm_service,
    )

    print("RESULT:")
    print(result)

    print("\nSYMPTOMS:")
    print(result["symptoms"])


if __name__ == "__main__":
    main()