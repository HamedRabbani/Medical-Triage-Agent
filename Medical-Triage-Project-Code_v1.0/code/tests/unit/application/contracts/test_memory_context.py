from application.contracts.memory_context import (
    MemoryContext,
)
from application.contracts.short_term_memory import (
    ShortTermMemory,
)


def test_memory_context_defaults():

    memory = ShortTermMemory(
        session_id=10,
    )

    context = MemoryContext(
        short_term=memory,
    )

    assert context.short_term.session_id == 10
    assert context.patient_profile is None
    assert context.medical_history == []
    assert context.previous_triage_results == []