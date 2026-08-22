from infrastructure.database.session import SessionLocal
from infrastructure.database.unit_of_work import UnitOfWork

from application.services.triage_service import TriageService
from infrastructure.database.repositories.sql_triage_persistence_repository import (
    SQLTriagePersistenceRepository,
)

def test_persian_storage():
    with SessionLocal() as session:

        uow = UnitOfWork(session)

        persistence = SQLTriagePersistenceRepository(uow)

        triage_service = TriageService(
            persistence
        )

        triage_session = triage_service.start_session(2)

        session.flush()

        message = triage_service.add_message(
            session_id=triage_session.session_id,
            sender_type="Patient",
            content="زیاد",
        )

        uow.commit()

        messages = uow.triage.get_messages(
            triage_session.session_id
        )

        print("Stored:", messages[0].content)

        assert messages[0].content == "زیاد"

        print("Persian Unicode storage PASSED.")


if __name__ == "__main__":
    test_persian_storage()