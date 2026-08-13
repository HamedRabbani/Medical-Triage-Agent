from .session import SessionLocal
from .unit_of_work import UnitOfWork


def test_unit_of_work() -> None:
    with SessionLocal() as session:

        with UnitOfWork(session) as uow:

            users = uow.users.get_all()
            patients = uow.patients.get_all()
            records = uow.medical_records.get_all()
            sessions = uow.triage.get_all()

            print(f"Users: {len(users)}")
            print(f"Patients: {len(patients)}")
            print(f"Medical records: {len(records)}")
            print(f"Triage sessions: {len(sessions)}")

        print("Unit of Work commit successful.")


if __name__ == "__main__":
    test_unit_of_work()