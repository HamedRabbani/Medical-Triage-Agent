from pydantic import BaseModel

from application.ports.llm_port import LLMPort
from application.contracts.llm_test_response import LLMTestResponse


class LLMService:

    def __init__(self, llm: LLMPort) -> None:
        self._llm = llm

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:

        return self._llm.generate(
            prompt,
            system_prompt=system_prompt,
        )

    def generate_structured(
        self,
        prompt: str,
        response_model: type[BaseModel],
        *,
        system_prompt: str | None = None,
    ) -> BaseModel:

        return self._llm.generate_structured(
            prompt,
            response_model,
            system_prompt=system_prompt,
        )

    def extract_symptoms(
        self,
        text: str,
    ) -> LLMTestResponse:

        prompt = f"""
Extract all symptoms explicitly present in the patient text.

Rules:
- Return only symptoms explicitly mentioned.
- Do not infer or add symptoms.
- Translate Persian symptoms to standard English medical names.
- Use lowercase English names.
- If no symptom is present, return an empty list.
- Preserve all explicitly mentioned symptoms.

Examples:
"من سردرد دارم" → ["headache"]
"من تب و سردرد دارم" → ["fever", "headache"]
"I have fever and a cough" → ["fever", "cough"]
"قفسه سینه‌ام درد می‌کند" → ["chest pain"]
"حالم خوب نیست" → []

Patient text:
{text}
"""

        return self.generate_structured(
            prompt,
            LLMTestResponse,
        )