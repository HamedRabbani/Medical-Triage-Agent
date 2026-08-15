from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.short_term_memory import (
    ShortTermMemory,
)
from application.services.conversation_service import (
    ConversationService,
)


class ShortTermMemoryService:
    """Build and update short-term memory."""

    def __init__(
        self,
        conversation_service: ConversationService | None = None,
    ):
        self.conversation_service = conversation_service

    def load(
        self,
        session_id: int,
    ) -> ShortTermMemory:
        """Load short-term memory for a session."""

        if self.conversation_service is None:
            raise ValueError(
                "ConversationService is required to load memory."
            )

        history = self.conversation_service.get_history(
            session_id
        )

        return ShortTermMemory(
            session_id=session_id,
            recent_messages=history,
            medical_context=ConversationExtraction(),
        )

    def update(
        self,
        memory: ShortTermMemory,
        extraction: ConversationExtraction,
    ) -> ShortTermMemory:
        """Merge newly extracted medical information."""

        medical = memory.medical_context

        symptoms = list(medical.symptoms)

        for symptom in extraction.symptoms:
            if symptom not in symptoms:
                symptoms.append(symptom)

        red_flags = list(medical.red_flags)

        for flag in extraction.red_flags:
            if flag not in red_flags:
                red_flags.append(flag)

        return ShortTermMemory(
            session_id=memory.session_id,
            recent_messages=memory.recent_messages,
            intent=memory.intent,
            medical_context=ConversationExtraction(
                symptoms=symptoms,
                severity=(
                    extraction.severity
                    if extraction.severity is not None
                    else medical.severity
                ),
                age=(
                    extraction.age
                    if extraction.age is not None
                    else medical.age
                ),
                duration=(
                    extraction.duration
                    if extraction.duration is not None
                    else medical.duration
                ),
                red_flags=red_flags,
            ),
        )