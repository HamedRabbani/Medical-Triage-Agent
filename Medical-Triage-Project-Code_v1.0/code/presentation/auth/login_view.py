
import streamlit as st

from application.services.patient_service import (
    PatientService,
)

from infrastructure.auth.auth_factory import (
    create_login_service,
)

from infrastructure.database.session import (
    SessionLocal,
)

from infrastructure.database.unit_of_work import (
    UnitOfWork,
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
    # Authenticate
    # ========================================================

    login_service, session = create_login_service()

    try:

        result = login_service.login(
            email=email.strip(),
            password=password,
        )

    finally:

        session.close()

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
        for role in (result.roles or [])
    ]

    # ========================================================
    # Default Session State
    # ========================================================

    st.session_state.authenticated = True

    st.session_state.user_id = result.user_id

    st.session_state.email = result.email

    st.session_state.roles = roles

    # Always initialize patient_id
    st.session_state.patient_id = None

    # ========================================================
    # Patient Profile Resolution
    # ONLY FOR PATIENT USERS
    # ========================================================

    if "patient" in roles:

        patient_session = SessionLocal()

        try:

            uow = UnitOfWork(patient_session)

            patient_service = PatientService(uow)

            patient = patient_service.get_patient_by_user_id(
                result.user_id
            )

        finally:

            patient_session.close()

        # ----------------------------------------------------
        # Patient profile must exist
        # ----------------------------------------------------

        if patient is None:

            st.session_state.authenticated = False

            st.error(
                "Patient profile not found. "
                "Please contact administrator."
            )

            return False

        # ----------------------------------------------------
        # Store Patient ID
        # ----------------------------------------------------

        st.session_state.patient_id = (
            patient.patient_id
        )

    # ========================================================
    # Authentication Context Validation
    # ========================================================

    if "patient" in roles:

        if st.session_state.patient_id is None:

            st.session_state.authenticated = False

            st.error(
                "Patient authentication context could not "
                "be initialized."
            )

            return False

    # ========================================================
    # DEBUG
    # Temporary: remove after confirming the flow
    # ========================================================

    st.write(
        "DEBUG user_id:",
        st.session_state.get("user_id"),
    )

    st.write(
        "DEBUG patient_id:",
        st.session_state.get("patient_id"),
    )

    st.write(
        "DEBUG roles:",
        st.session_state.get("roles"),
    )

    # ========================================================
    # Login Success
    # ========================================================

    st.success(
        "Login successful."
    )

    st.rerun()

    return True

