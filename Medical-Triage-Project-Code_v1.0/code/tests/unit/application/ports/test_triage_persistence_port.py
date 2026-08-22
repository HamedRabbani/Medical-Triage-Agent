from unittest.mock import Mock

from application.ports.triage_persistence_port import (
    TriagePersistencePort,
)


def test_triage_persistence_contract():
    repository = Mock()

    assert hasattr(
        repository,
        "patient_exists",
    )

    assert hasattr(
        repository,
        "create_session",
    )

    assert hasattr(
        repository,
        "get_session",
    )

    assert hasattr(
        repository,
        "add_message",
    )

    assert hasattr(
        repository,
        "add_result",
    )

    assert hasattr(
        repository,
        "commit",
    )

    assert hasattr(
        repository,
        "rollback",
    )