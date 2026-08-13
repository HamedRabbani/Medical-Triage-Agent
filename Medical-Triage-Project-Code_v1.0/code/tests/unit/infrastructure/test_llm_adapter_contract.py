# tests/unit/infrastructure/test_llm_adapter_contract.py

from application.ports.llm_port import LLMPort


def verify_llm_contract(llm: LLMPort) -> None:

    result = llm.generate(
        "Say hello in one sentence."
    )

    assert isinstance(result, str)
    assert result.strip()