from application.ports.llm_port import LLMPort


class FakeLLM(LLMPort):

    def generate(self, prompt: str) -> str:
        return f"Fake response: {prompt}"


def test_llm_port_contract():
    llm = FakeLLM()

    result = llm.generate("Hello")

    assert result == "Fake response: Hello"