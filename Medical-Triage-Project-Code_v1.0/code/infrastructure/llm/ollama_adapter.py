from ollama import Client
from pydantic import BaseModel

from application.ports.llm_port import LLMPort


class OllamaAdapter(LLMPort):

    def __init__(
        self,
        model: str,
        host: str = "http://localhost:11434",
    ) -> None:
        self._client = Client(host=host)
        self._model = model

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self._client.chat(
            model=self._model,
            messages=messages,
        )

        return response.message.content

    def generate_structured(
        self,
        prompt: str,
        response_model: type[BaseModel],
        *,
        system_prompt: str | None = None,
    ) -> BaseModel:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self._client.chat(
            model=self._model,
            messages=messages,
            format=response_model.model_json_schema(),
        )

        return response_model.model_validate_json(
            response.message.content
        )