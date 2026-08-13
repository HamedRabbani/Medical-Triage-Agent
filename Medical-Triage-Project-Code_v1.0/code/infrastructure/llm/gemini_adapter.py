from google import genai
from google.genai import types
from pydantic import BaseModel

from application.ports.llm_port import LLMPort


class GeminiAdapter(LLMPort):

    def __init__(
        self,
        api_key: str,
        model: str,
    ) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:

        config = None

        if system_prompt:
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
            )

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config=config,
        )

        return response.text

    def generate_structured(
        self,
        prompt: str,
        response_model: type[BaseModel],
        *,
        system_prompt: str | None = None,
    ) -> BaseModel:

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_model,
        )

        if system_prompt:
            config.system_instruction = system_prompt

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config=config,
        )

        if response.parsed is not None:
            return response.parsed

        return response_model.model_validate_json(response.text)