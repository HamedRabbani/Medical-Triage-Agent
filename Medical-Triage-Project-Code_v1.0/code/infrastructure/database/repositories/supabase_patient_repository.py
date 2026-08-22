from application.ports.patient_port import PatientPort


class SupabasePatientRepository(PatientPort):
    """Supabase implementation of patient persistence."""

    def __init__(self, client):
        self.client = client

    def get_patient_by_id(
        self,
        patient_id: int,
    ):
        response = (
            self.client
            .table("PatientProfile")
            .select(
                "PatientId,UserId,FirstName,LastName,"
                "DateOfBirth,Gender,NationalId,CreatedAt"
            )
            .eq("PatientId", patient_id)
            .limit(1)
            .execute()
        )

        rows = response.data or []

        if not rows:
            return None

        return _PatientRecord.from_row(
            rows[0]
        )

    def get_patient_by_user_id(
        self,
        user_id: int,
    ):
        response = (
            self.client
            .table("PatientProfile")
            .select(
                "PatientId,UserId,FirstName,LastName,"
                "DateOfBirth,Gender,NationalId,CreatedAt"
            )
            .eq("UserId", user_id)
            .limit(1)
            .execute()
        )

        rows = response.data or []

        if not rows:
            return None

        return _PatientRecord.from_row(
            rows[0]
        )


class _PatientRecord:

    def __init__(
        self,
        patient_id,
        user_id,
        first_name=None,
        last_name=None,
        date_of_birth=None,
        gender=None,
        national_id=None,
        created_at=None,
    ):
        self.patient_id = patient_id
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.national_id = national_id
        self.created_at = created_at

    @classmethod
    def from_row(
        cls,
        row: dict,
    ):
        return cls(
            patient_id=row["PatientId"],
            user_id=row["UserId"],
            first_name=row.get("FirstName"),
            last_name=row.get("LastName"),
            date_of_birth=row.get("DateOfBirth"),
            gender=row.get("Gender"),
            national_id=row.get("NationalId"),
            created_at=row.get("CreatedAt"),
        )