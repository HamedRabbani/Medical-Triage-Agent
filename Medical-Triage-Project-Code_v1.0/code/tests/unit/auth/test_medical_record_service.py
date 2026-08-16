from types import SimpleNamespace

from application.auth.authorization_service import (
    AuthorizationService,
)
from application.services.medical_record_service import (
    MedicalRecordService,
)


def make_user(role: str, user_id: int):
    return SimpleNamespace(
        user_id=user_id,
        user_roles=[
            SimpleNamespace(
                role=SimpleNamespace(
                    role_name=role,
                ),
            )
        ],
    )


def make_uow(
    record=None,
    patient=None,
    patients=None,
    doctor=None,
    doctor_can_access=False,
    records=None,
):
    patient_map = patients or {}

    if patient is not None:
        patient_map[patient.patient_id] = patient

    medical_record_repository = SimpleNamespace(
        get_by_id=lambda record_id: record,
        get_by_patient_id=lambda patient_id: (
            records if records is not None else []
        ),
    )

    patient_repository = SimpleNamespace(
        get_by_id=lambda patient_id: patient_map.get(patient_id),
    )

    doctor_repository = SimpleNamespace(
        get_by_user_id=lambda user_id: doctor,
        can_access_patient=lambda doctor_id, patient_id: (
            doctor_can_access
        ),
    )

    return SimpleNamespace(
        medical_records=medical_record_repository,
        patients=patient_repository,
        doctors=doctor_repository,
    )


# =========================================================
# Single Medical Record Access
# =========================================================


def test_patient_can_access_own_medical_record():

    patient = SimpleNamespace(
        patient_id=100,
        user_id=20,
    )

    record = SimpleNamespace(
        record_id=1,
        patient_id=100,
    )

    user = make_user(
        AuthorizationService.PATIENT,
        20,
    )

    service = MedicalRecordService(
        make_uow(
            record=record,
            patient=patient,
        )
    )

    result = service.get_record(
        user,
        1,
    )

    assert result is record


def test_patient_cannot_access_another_patient_medical_record():

    own_patient = SimpleNamespace(
        patient_id=100,
        user_id=20,
    )

    another_patient = SimpleNamespace(
        patient_id=200,
        user_id=30,
    )

    record = SimpleNamespace(
        record_id=2,
        patient_id=200,
    )

    user = make_user(
        AuthorizationService.PATIENT,
        20,
    )

    service = MedicalRecordService(
        make_uow(
            record=record,
            patients={
                100: own_patient,
                200: another_patient,
            },
        )
    )

    result = service.get_record(
        user,
        2,
    )

    assert result is None


def test_doctor_can_access_assigned_patient_record():

    doctor = SimpleNamespace(
        doctor_id=10,
        user_id=20,
    )

    record = SimpleNamespace(
        record_id=3,
        patient_id=100,
    )

    user = make_user(
        AuthorizationService.DOCTOR,
        20,
    )

    service = MedicalRecordService(
        make_uow(
            record=record,
            doctor=doctor,
            doctor_can_access=True,
        )
    )

    result = service.get_record(
        user,
        3,
    )

    assert result is record


def test_doctor_cannot_access_unassigned_patient_record():

    doctor = SimpleNamespace(
        doctor_id=10,
        user_id=20,
    )

    record = SimpleNamespace(
        record_id=4,
        patient_id=200,
    )

    user = make_user(
        AuthorizationService.DOCTOR,
        20,
    )

    service = MedicalRecordService(
        make_uow(
            record=record,
            doctor=doctor,
            doctor_can_access=False,
        )
    )

    result = service.get_record(
        user,
        4,
    )

    assert result is None


def test_system_admin_can_access_any_medical_record():

    record = SimpleNamespace(
        record_id=5,
        patient_id=300,
    )

    user = make_user(
        AuthorizationService.SYSTEM_ADMIN,
        999,
    )

    service = MedicalRecordService(
        make_uow(
            record=record,
        )
    )

    result = service.get_record(
        user,
        5,
    )

    assert result is record


def test_hospital_admin_cannot_access_unrestricted_medical_record():

    record = SimpleNamespace(
        record_id=6,
        patient_id=400,
    )

    user = make_user(
        AuthorizationService.HOSPITAL_ADMIN,
        50,
    )

    service = MedicalRecordService(
        make_uow(
            record=record,
        )
    )

    result = service.get_record(
        user,
        6,
    )

    assert result is None


# =========================================================
# Patient Medical Records
# =========================================================


def test_patient_can_get_own_medical_records():

    patient = SimpleNamespace(
        patient_id=100,
        user_id=20,
    )

    records = [
        SimpleNamespace(
            record_id=1,
            patient_id=100,
        ),
        SimpleNamespace(
            record_id=2,
            patient_id=100,
        ),
    ]

    user = make_user(
        AuthorizationService.PATIENT,
        20,
    )

    service = MedicalRecordService(
        make_uow(
            patient=patient,
            records=records,
        )
    )

    result = service.get_patient_records(
        user,
        100,
    )

    assert result == records


def test_patient_cannot_get_another_patient_records():

    own_patient = SimpleNamespace(
        patient_id=100,
        user_id=20,
    )

    another_patient = SimpleNamespace(
        patient_id=200,
        user_id=30,
    )

    records = [
        SimpleNamespace(
            record_id=3,
            patient_id=200,
        ),
    ]

    user = make_user(
        AuthorizationService.PATIENT,
        20,
    )

    service = MedicalRecordService(
        make_uow(
            patients={
                100: own_patient,
                200: another_patient,
            },
            records=records,
        )
    )

    result = service.get_patient_records(
        user,
        200,
    )

    assert result == []


# =========================================================
# Doctor Medical Records
# =========================================================


def test_doctor_can_get_assigned_patient_records():

    doctor = SimpleNamespace(
        doctor_id=10,
        user_id=20,
    )

    records = [
        SimpleNamespace(
            record_id=4,
            patient_id=100,
        ),
    ]

    user = make_user(
        AuthorizationService.DOCTOR,
        20,
    )

    service = MedicalRecordService(
        make_uow(
            doctor=doctor,
            doctor_can_access=True,
            records=records,
        )
    )

    result = service.get_patient_records(
        user,
        100,
    )

    assert result == records


def test_doctor_cannot_get_unassigned_patient_records():

    doctor = SimpleNamespace(
        doctor_id=10,
        user_id=20,
    )

    records = [
        SimpleNamespace(
            record_id=5,
            patient_id=200,
        ),
    ]

    user = make_user(
        AuthorizationService.DOCTOR,
        20,
    )

    service = MedicalRecordService(
        make_uow(
            doctor=doctor,
            doctor_can_access=False,
            records=records,
        )
    )

    result = service.get_patient_records(
        user,
        200,
    )

    assert result == []