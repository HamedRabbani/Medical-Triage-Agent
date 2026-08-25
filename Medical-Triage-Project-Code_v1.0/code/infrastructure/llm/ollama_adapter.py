from typing import Any, TypeVar

from ollama import Client
from pydantic import BaseModel

from application.ports.llm_port import LLMPort


T = TypeVar("T", bound=BaseModel)


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
            keep_alive="30m",
            options={
                "num_ctx": 2048,
                "num_predict": 128,
            },
        )

        return response.message.content

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        *,
        system_prompt: str | None = None,
    ) -> T:

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
            keep_alive="30m",
        )

        raw_content = response.message.content

        normalized_content = self._normalize_structured_response(
            raw_content
        )

        return response_model.model_validate_json(
            normalized_content
        )

    @staticmethod
    def _normalize_structured_response(
        content: str,
    ) -> str:
        """
        Normalize harmless floating-point boundary artifacts
        before Pydantic validation.

        Example:
            1.0000000000000004 -> 1.0

        Only numeric values slightly outside the valid [0, 1]
        probability boundary are corrected.
        """

        import json
        import math

        if not isinstance(content, str):
            raise TypeError(
                "Ollama structured response must be a string."
            )

        data: Any = json.loads(content)

        if isinstance(data, dict):
            confidence = data.get("confidence")

            if isinstance(
                confidence,
                (int, float),
            ) and not isinstance(
                confidence,
                bool,
            ):
                if (
                    math.isfinite(confidence)
                    and confidence > 1.0
                    and confidence <= 1.000001
                ):
                    data["confidence"] = 1.0

                elif (
                    math.isfinite(confidence)
                    and confidence < 0.0
                    and confidence >= -0.000001
                ):
                    data["confidence"] = 0.0

        return json.dumps(
            data,
            ensure_ascii=False,
        )