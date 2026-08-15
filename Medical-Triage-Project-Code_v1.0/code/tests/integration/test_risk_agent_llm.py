from application.config.llm_config import LLMConfig
from application.services.llm_service import LLMService
from infrastructure.llm.llm_factory import create_llm
from agents.risk_agent import risk_agent

def test_risk_agent_with_real_llm():

    config = LLMConfig(
        provider="ollama",
        model="gemma3",
    )

    llm = create_llm(config)

    llm_service = LLMService(llm)

    state = {
        "symptoms": ["chest pain"],
        "severity": "severe",
        "age": 29,
        "duration": "20 minutes",
    }

    result = risk_agent(
        state,
        llm_service=llm_service,
    )

    print("\n=== REAL LLM RISK TEST ===")

    print(
        "Rule:",
        result["risk_level"],
        result["confidence"],
    )

    print(
        "LLM:",
        result["llm_risk_level"],
        result["llm_confidence"],
    )

    print(
        "LLM Red Flags:",
        result["llm_red_flags"],
    )

    print(
        "LLM Recommendation:",
        result["llm_recommendation"],
    )

    assert result["risk_level"] in {
        "LOW",
        "HIGH",
    }

    assert result["llm_risk_level"] in {
        "LOW",
        "HIGH",
    }

    assert 0.0 <= result["llm_confidence"] <= 1.0