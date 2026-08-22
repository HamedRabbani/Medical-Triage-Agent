from application.config.settings import Settings

from infrastructure.database.repositories.supabase_triage_persistence_repository import (
    SupabaseTriagePersistenceRepository,
)
from infrastructure.database.repositories.supabase_conversation_history_repository import (
    SupabaseConversationHistoryRepository,
)

from supabase import create_client


def test_supabase_write_read_cleanup():
    settings = Settings(
        _env_file=".env",
        db_backend="supabase",
    )

    client = create_client(
        settings.supabase_url,
        settings.supabase_key,
    )

    triage_repository = (
        SupabaseTriagePersistenceRepository(
            client
        )
    )

    conversation_repository = (
        SupabaseConversationHistoryRepository(
            client
        )
    )

    # ---------------------------------------------------------
    # 1. Find an existing patient in Supabase
    # ---------------------------------------------------------

    response = (
        client
        .table("PatientProfile")
        .select("PatientId")
        .limit(1)
        .execute()
    )

    patients = response.data or []

    assert patients, (
        "No patient exists in Supabase PatientProfile."
    )

    patient_id = patients[0]["PatientId"]

    assert triage_repository.patient_exists(
        patient_id
    ) is True

    # ---------------------------------------------------------
    # 2. Create session
    # ---------------------------------------------------------

    session = triage_repository.create_session(
        patient_id
    )

    session_id = session.session_id

    assert session_id is not None

    try:
        # -----------------------------------------------------
        # 3. Add message
        # -----------------------------------------------------

        message = triage_repository.add_message(
            session_id=session_id,
            sender_type="Patient",
            content="Supabase integration test",
        )

        assert message.session_id == session_id

        # -----------------------------------------------------
        # 4. Read history
        # -----------------------------------------------------

        history = conversation_repository.get_history(
            session_id
        )

        assert isinstance(
            history,
            list,
        )

        assert any(
            item["content"]
            == "Supabase integration test"
            for item in history
        )

        # -----------------------------------------------------
        # 5. Add triage result
        # -----------------------------------------------------

        result = triage_repository.add_result(
            session_id=session_id,
            risk_level="LOW",
            confidence_score=0.99,
            recommendation="Integration test only.",
        )

        assert result.session_id == session_id
        assert result.risk_level == "LOW"
        assert result.confidence_score == 0.99

    finally:
        # -----------------------------------------------------
        # 6. Cleanup
        # -----------------------------------------------------

        client.table(
            "TriageResult"
        ).delete().eq(
            "SessionId",
            session_id,
        ).execute()

        client.table(
            "ConversationMsg"
        ).delete().eq(
            "SessionId",
            session_id,
        ).execute()

        client.table(
            "TriageSession"
        ).delete().eq(
            "SessionId",
            session_id,
        ).execute()