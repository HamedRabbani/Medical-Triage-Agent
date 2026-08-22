from unittest.mock import Mock

from infrastructure.database.repositories.supabase_triage_persistence_repository import (
    SupabaseTriagePersistenceRepository,
)


def _configure_query_chain(client):
    query = client.table.return_value

    query.select.return_value = query
    query.eq.return_value = query
    query.limit.return_value = query
    query.insert.return_value = query
    query.order.return_value = query

    return query


def test_patient_exists():
    client = Mock()

    query = _configure_query_chain(client)

    query.execute.return_value = Mock(
        data=[
            {
                "PatientId": 2,
            }
        ]
    )

    repository = SupabaseTriagePersistenceRepository(
        client
    )

    assert repository.patient_exists(2) is True


def test_patient_does_not_exist():
    client = Mock()

    query = _configure_query_chain(client)

    query.execute.return_value = Mock(
        data=[]
    )

    repository = SupabaseTriagePersistenceRepository(
        client
    )

    assert repository.patient_exists(999) is False


def test_create_session():
    client = Mock()

    query = _configure_query_chain(client)

    query.execute.return_value = Mock(
        data=[
            {
                "SessionId": 10,
                "PatientId": 2,
                "Status": "Active",
            }
        ]
    )

    repository = SupabaseTriagePersistenceRepository(
        client
    )

    result = repository.create_session(2)

    assert result.session_id == 10
    assert result.patient_id == 2
    assert result.status == "Active"


def test_get_session():
    client = Mock()

    query = _configure_query_chain(client)

    query.execute.return_value = Mock(
        data=[
            {
                "SessionId": 10,
                "PatientId": 2,
                "StartTime": None,
                "EndTime": None,
                "Status": "Active",
            }
        ]
    )

    repository = SupabaseTriagePersistenceRepository(
        client
    )

    result = repository.get_session(10)

    assert result is not None
    assert result.session_id == 10
    assert result.patient_id == 2


def test_get_missing_session():
    client = Mock()

    query = _configure_query_chain(client)

    query.execute.return_value = Mock(
        data=[]
    )

    repository = SupabaseTriagePersistenceRepository(
        client
    )

    assert repository.get_session(999) is None


def test_add_message():
    client = Mock()

    query = _configure_query_chain(client)

    query.execute.return_value = Mock(
        data=[
            {
                "MessageId": 20,
                "SessionId": 10,
                "SenderType": "Patient",
                "Content": "زیاد",
            }
        ]
    )

    repository = SupabaseTriagePersistenceRepository(
        client
    )

    result = repository.add_message(
        session_id=10,
        sender_type="Patient",
        content="زیاد",
    )

    assert result.message_id == 20
    assert result.session_id == 10
    assert result.sender_type == "Patient"
    assert result.content == "زیاد"


def test_add_result():
    client = Mock()

    query = _configure_query_chain(client)

    query.execute.return_value = Mock(
        data=[
            {
                "ResultId": 30,
                "SessionId": 10,
                "RiskLevel": "HIGH",
                "ConfidenceScore": 0.95,
                "Recommendation": (
                    "Seek immediate medical attention."
                ),
            }
        ]
    )

    repository = SupabaseTriagePersistenceRepository(
        client
    )

    result = repository.add_result(
        session_id=10,
        risk_level="HIGH",
        confidence_score=0.95,
        recommendation=(
            "Seek immediate medical attention."
        ),
    )

    assert result.result_id == 30
    assert result.session_id == 10
    assert result.risk_level == "HIGH"
    assert result.confidence_score == 0.95
    assert (
        result.recommendation
        == "Seek immediate medical attention."
    )


def test_commit_and_rollback_are_safe_noops():
    client = Mock()

    repository = SupabaseTriagePersistenceRepository(
        client
    )

    repository.commit()
    repository.rollback()