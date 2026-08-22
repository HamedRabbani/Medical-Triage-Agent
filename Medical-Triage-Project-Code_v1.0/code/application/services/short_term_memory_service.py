from application.contracts.conversation_extraction import (
    ConversationExtraction,
)
from application.contracts.short_term_memory import (
    ShortTermMemory,
)
from application.ports.memory_port import MemoryPort


class ShortTermMemoryService(MemoryPort):
    """Build and update session-scoped short-term memory."""

    def load(
        self,
        session_id: int,
        history: list[dict],
    ) -> ShortTermMemory:
        """Reconstruct short-term memory from persisted conversation."""

        return ShortTermMemory(
            session_id=session_id,
            recent_messages=list(history),
            medical_context=ConversationExtraction(),
        )

    def update(
        self,
        memory: ShortTermMemory,
        extraction: ConversationExtraction,
    ) -> ShortTermMemory:
        """Merge newly extracted information into current memory."""

        medical = memory.medical_context

        symptoms = list(medical.symptoms)

        for symptom in extraction.symptoms:
            if symptom not in symptoms:
                symptoms.append(symptom)

        red_flags = list(medical.red_flags)

        for flag in extraction.red_flags:
            if flag not in red_flags:
                red_flags.append(flag)

        updated_context = ConversationExtraction(
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
        )

        return ShortTermMemory(
            session_id=memory.session_id,
            recent_messages=list(memory.recent_messages),
            intent=memory.intent,
            medical_context=updated_context,
        )