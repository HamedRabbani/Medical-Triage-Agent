from unittest.mock import Mock

from infrastructure.database.repositories.sql_triage_persistence_repository import (
    SQLTriagePersistenceRepository,
)


def test_patient_exists():
    uow = Mock()

    uow.patients.get_by_id.return_value = Mock()

    repository = SQLTriagePersistenceRepository(
        uow
    )

    result = repository.patient_exists(
        patient_id=2
    )

    assert result is True

    uow.patients.get_by_id.assert_called_once_with(
        2
    )


def test_patient_does_not_exist():
    uow = Mock()

    uow.patients.get_by_id.return_value = None

    repository = SQLTriagePersistenceRepository(
        uow
    )

    result = repository.patient_exists(
        patient_id=999
    )

    assert result is False

    uow.patients.get_by_id.assert_called_once_with(
        999
    )


def test_create_session():
    uow = Mock()

    repository = SQLTriagePersistenceRepository(
        uow
    )

    result = repository.create_session(
        patient_id=2
    )

    assert result.patient_id == 2
    assert result.status == "Active"

    uow.triage.add.assert_called_once_with(
        result
    )


def test_get_session():
    uow = Mock()

    expected_session = Mock()

    uow.triage.get_by_id.return_value = (
        expected_session
    )

    repository = SQLTriagePersistenceRepository(
        uow
    )

    result = repository.get_session(
        session_id=10
    )

    assert result is expected_session

    uow.triage.get_by_id.assert_called_once_with(
        10
    )


def test_add_message():
    uow = Mock()

    repository = SQLTriagePersistenceRepository(
        uow
    )

    result = repository.add_message(
        session_id=10,
        sender_type="Patient",
        content="زیاد",
    )

    assert result.session_id == 10
    assert result.sender_type == "Patient"
    assert result.content == "زیاد"

    uow.triage.add_message.assert_called_once_with(
        result
    )


def test_add_result():
    uow = Mock()

    repository = SQLTriagePersistenceRepository(
        uow
    )

    result = repository.add_result(
        session_id=10,
        risk_level="HIGH",
        confidence_score=0.95,
        recommendation="Seek immediate medical attention.",
    )

    assert result.session_id == 10
    assert result.risk_level == "HIGH"
    assert result.confidence_score == 0.95
    assert (
        result.recommendation
        == "Seek immediate medical attention."
    )

    uow.triage.add_result.assert_called_once_with(
        result
    )


def test_commit():
    uow = Mock()

    repository = SQLTriagePersistenceRepository(
        uow
    )

    repository.commit()

    uow.commit.assert_called_once_with()


def test_rollback():
    uow = Mock()

    repository = SQLTriagePersistenceRepository(
        uow
    )

    repository.rollback()

    uow.rollback.assert_called_once_with()