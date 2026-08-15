from application.config.llm_config import LLMConfig
from application.services.llm_service import LLMService
from infrastructure.llm.llm_factory import create_llm

from agents.risk_agent import risk_agent
from agents.supervisor_agent import supervisor_agent


def test_supervisor_with_real_llm():

    config = LLMConfig(
        provider="ollama",
        model="gemma3",
    )

    llm = create_llm(config)
    llm_service = LLMService(llm)

    state = {
        "symptoms": [
            "chest pain",
        ],
        "severity": "severe",
        "age": 29,
        "duration": "20 minutes",
    }

    # -------------------------
    # Risk Agent
    # -------------------------

    state = risk_agent(
        state,
        llm_service=llm_service,
    )

    # -------------------------
    # Supervisor
    # -------------------------

    result = supervisor_agent(state)

    print("\n=== REAL LLM SUPERVISOR TEST ===")

    print(
        "Rule Risk:",
        result.get("risk_level"),
    )

    print(
        "LLM Risk:",
        result.get("llm_risk_level"),
    )

    print(
        "Rule Confidence:",
        result.get("confidence"),
    )

    print(
        "LLM Confidence:",
        result.get("llm_confidence"),
    )

    print(
        "Supervisor Status:",
        result.get("supervisor_status"),
    )

    print(
        "Red Flags:",
        result.get("red_flags"),
    )

    # -------------------------
    # Assertions
    # -------------------------

    assert result["risk_level"] in {
        "LOW",
        "HIGH",
    }

    assert result["llm_risk_level"] in {
        "LOW",
        "HIGH",
    }

    assert result["supervisor_status"] in {
        "APPROVED",
        "REVIEW_REQUIRED",
        "REJECTED",
    }