import streamlit as st

from application.config.settings import Settings
from application.services.patient_service import (
    PatientService,
)

from infrastructure.auth.auth_factory import (
    create_login_service,
)

from infrastructure.database.conversation_persistence_factory import (
    create_database_backend,
)


def render_login() -> bool:
    """
    Render login page.

    Authentication flow:

        UserAccount
            ↓
        LoginService
            ↓
        Resolve Roles
            ↓
        PatientService for Patient users
            ↓
        Streamlit Session State
    """

    st.title("Medical AI Triage")
    st.subheader("Login / ورود")

    # ========================================================
    # Login Form
    # ========================================================

    with st.form("login_form"):

        email = st.text_input(
            "Email",
            placeholder="example@email.com",
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Login / ورود",
            use_container_width=True,
        )

    if not submitted:
        return False

    if not email.strip() or not password:

        st.error(
            "Email and password are required."
        )

        return False

    # ========================================================
    # Configuration
    # ========================================================

    settings = Settings()

    # ========================================================
    # Authentication
    # ========================================================

    login_service, auth_resource = (
        create_login_service(settings)
    )

    try:

        result = login_service.login(
            email=email.strip(),
            password=password,
        )

    finally:

        if auth_resource is not None:
            auth_resource.close()

    # ========================================================
    # Authentication Failure
    # ========================================================

    if not result.success:

        st.error(
            result.error
            or "Login failed."
        )

        return False

    # ========================================================
    # Normalize Roles
    # ========================================================

    roles = [
        str(role).lower()
        for role in (
            result.roles or []
        )
    ]

    # ========================================================
    # Default Session State
    # ========================================================

    st.session_state.authenticated = True

    st.session_state.user_id = (
        result.user_id
    )

    st.session_state.email = (
        result.email
    )

    st.session_state.roles = roles

    st.session_state.patient_id = None

    # ========================================================
    # Patient Profile Resolution
    # ONLY FOR PATIENT USERS
    # ========================================================

    database_backend = None

    if "patient" in roles:

        database_backend = (
            create_database_backend(
                settings
            )
        )

        try:

            patient_service = PatientService(
                database_backend.patient
            )

            patient = (
                patient_service
                .get_patient_by_user_id(
                    result.user_id
                )
            )

        except Exception:

            database_backend.close()

            st.session_state.authenticated = False

            st.error(
                "Patient profile could not be loaded."
            )

            return False

        if patient is None:

            database_backend.close()

            st.session_state.authenticated = False

            st.error(
                "Patient profile not found. "
                "Please contact administrator."
            )

            return False

        st.session_state.patient_id = (
            patient.patient_id
        )

        database_backend.close()

    # ========================================================
    # Authentication Context Validation
    # ========================================================

    if "patient" in roles:

        if (
            st.session_state.patient_id
            is None
        ):

            st.session_state.authenticated = False

            st.error(
                "Patient authentication context "
                "could not be initialized."
            )

            return False

    

    # ========================================================
    # Login Success
    # ========================================================

    st.success(
        "Login successful."
    )

    st.rerun()

    return True