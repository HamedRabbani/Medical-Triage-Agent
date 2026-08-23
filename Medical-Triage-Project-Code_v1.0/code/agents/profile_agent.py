from application.services.patient_service import PatientService


def profile_agent(
    state,
    patient_service: PatientService,
):
    """
    Return the authenticated user's own profile.
    """

    user_id = state.get("user_id")

    if user_id is None:
        response = (
            "Unable to determine the authenticated user."
        )

        return {
            **state,
            "assistant_response": response,
            "response": response,
        }

    patient = patient_service.get_patient_by_user_id(
        user_id
    )

    if patient is None:
        response = (
            "No patient profile was found for your account."
        )

        return {
            **state,
            "assistant_response": response,
            "response": response,
        }

    response = (
        f"Patient ID: {patient.patient_id}\n"
        f"First name: {patient.first_name}\n"
        f"Last name: {patient.last_name}\n"
        f"Date of birth: {patient.date_of_birth}\n"
        f"Gender: {patient.gender}"
    )

    return {
        **state,
        "assistant_response": response,
        "response": response,
    }