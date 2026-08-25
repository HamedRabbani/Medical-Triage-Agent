from application.contracts.conversation_extraction import (
    ConversationExtraction,
)

from application.contracts.short_term_memory import (
    ShortTermMemory,
)

from application.ports.memory_port import (
    MemoryPort,
)


class ShortTermMemoryService(MemoryPort):
    """
    Build and update session-scoped short-term memory.
    """

    def load(
        self,
        session_id: int,
        history: list[dict],
    ) -> ShortTermMemory:
        """
        Reconstruct short-term memory from persisted
        conversation history.

        Medical information is reconstructed later by
        the conversation/medical extraction pipeline.
        """

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
        """
        Merge newly extracted information into the
        existing short-term memory.

        Existing information is preserved unless the
        new extraction explicitly provides a value.
        """

        medical = memory.medical_context

        # =====================================================
        # Symptoms
        # =====================================================

        symptoms = list(
            medical.symptoms
        )

        for symptom in extraction.symptoms:

            if symptom not in symptoms:

                symptoms.append(
                    symptom
                )

        # =====================================================
        # Red Flags
        # =====================================================

        red_flags = list(
            medical.red_flags
        )

        for flag in extraction.red_flags:

            if flag not in red_flags:

                red_flags.append(
                    flag
                )

        # =====================================================
        # Severity
        # =====================================================

        severity = (
            extraction.severity
            if extraction.severity is not None
            else medical.severity
        )

        # =====================================================
        # Age
        # =====================================================

        age = (
            extraction.age
            if extraction.age is not None
            else medical.age
        )

        # =====================================================
        # Duration
        # =====================================================

        duration = (
            extraction.duration
            if extraction.duration is not None
            else medical.duration
        )

        # =====================================================
        # Pain Location
        # =====================================================

        pain_location = (
            extraction.pain_location
            if extraction.pain_location is not None
            else medical.pain_location
        )

        # =====================================================
        # Updated Medical Context
        # =====================================================

        updated_context = ConversationExtraction(
            symptoms=symptoms,

            severity=severity,

            age=age,

            duration=duration,

            pain_location=pain_location,

            red_flags=red_flags,
        )

        # =====================================================
        # Return Updated Memory
        # =====================================================

        return ShortTermMemory(
            session_id=memory.session_id,

            recent_messages=list(
                memory.recent_messages
            ),

            intent=memory.intent,

            medical_context=updated_context,

            missing_information=list(
                memory.missing_information
            ),

            current_question=(
                memory.current_question
            ),

            risk_context=dict(
                memory.risk_context
            ),
        )