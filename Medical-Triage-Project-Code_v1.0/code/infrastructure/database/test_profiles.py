from .models import PatientProfile, DoctorProfile, HealthcareOrg
from .session import SessionLocal


# Test profile and organization relationships
def test_profiles() -> None:
    with SessionLocal() as session:

        # Test PatientProfile
        patients = session.query(PatientProfile).all()

        for patient in patients:
            print(
                f"Patient: "
                f"{patient.first_name} {patient.last_name}"
            )
            print(f"  User: {patient.user.email}")

        # Test HealthcareOrg
        organizations = session.query(HealthcareOrg).all()

        for organization in organizations:
            print(f"Organization: {organization.name}")

            for doctor in organization.doctors:
                print(f"  Doctor: {doctor.specialty}")
                print(f"  User: {doctor.user.email}")


if __name__ == "__main__":
    test_profiles()