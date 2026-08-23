from application.services.patient_service import PatientService


def profile_agent(
    state,
    patient_service: PatientService,
):
    """
    Return the authenticated user's own profile.
    """

    user_id = state.get(
        "user_id"
    )

    patient_id = state.get(
        "patient_id"
    )

    patient = None

    # =========================================================
    # Preferred: Load by user_id
    # =========================================================

    if user_id is not None:

        patient = (
            patient_service
            .get_patient_by_user_id(
                user_id
            )
        )

    # =========================================================
    # Fallback: Load by patient_id
    # =========================================================

    elif patient_id is not None:

        patient = (
            patient_service
            .get_patient(
                user=state.get("user"),
                patient_id=patient_id,
            )
            if state.get("user") is not None
            else patient_service.repository.get_patient_by_id(
                patient_id
            )
        )

    # =========================================================
    # No identity found
    # =========================================================

    if patient is None:

        response = (
            "No patient profile was found."
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