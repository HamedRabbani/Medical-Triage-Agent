import os

import streamlit as st


# ============================================================
# Streamlit Secrets -> Environment
# IMPORTANT:
# This must happen BEFORE importing the workflow graph.
# ============================================================

SECRET_KEYS = (
    "DB_BACKEND",
    "DATABASE_URL",
    "DIRECT_URL",
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "LLM_PROVIDER",
    "LLM_MODEL",
    "GEMINI_API_KEY",
    "OLLAMA_HOST",
)

for key in SECRET_KEYS:

    if key in st.secrets:

        os.environ[key] = str(
            st.secrets[key]
        )


# ============================================================
# Application Imports
# ============================================================

from workflow.triage_graph import triage_graph
from presentation.auth.login_view import render_login


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Medical AI Triage",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Authentication
# ============================================================

if not st.session_state.get(
    "authenticated",
    False,
):

    render_login()
    st.stop()


# ============================================================
# Session State
# ============================================================

def create_initial_state() -> dict:
    """
    Create the initial state for a new triage conversation.

    Authentication information is taken from Streamlit
    session state and passed into the LangGraph state.
    """

    return {

        # ----------------------------------------------------
        # Authentication Context
        # ----------------------------------------------------

        "user_id": st.session_state.get(
            "user_id"
        ),

        "patient_id": st.session_state.get(
            "patient_id"
        ),

        "user_roles": st.session_state.get(
            "roles",
            [],
        ),

        # ----------------------------------------------------
        # Triage Session
        # ----------------------------------------------------

        "session_id": None,

        # ----------------------------------------------------
        # User Input
        # ----------------------------------------------------

        "user_message": "",

        # ----------------------------------------------------
        # Patient Information
        # ----------------------------------------------------

        "age": None,

        "symptoms": [],

        "duration": None,

        "severity": None,

        # ----------------------------------------------------
        # Risk Assessment
        # ----------------------------------------------------

        "red_flags": [],

        "risk_level": None,

        "confidence": None,

        "recommendation": None,

        # ----------------------------------------------------
        # Planner
        # ----------------------------------------------------

        "missing_information": [],

        "next_question": None,

        # ----------------------------------------------------
        # Conversation
        # ----------------------------------------------------

        "conversation_history": [],

        "intent": None,

        "intent_confidence": None,

        "assistant_response": None,

        "response": None,

        # ----------------------------------------------------
        # Supervisor
        # ----------------------------------------------------

        "supervisor_status": None,

        # ----------------------------------------------------
        # Persistence
        # ----------------------------------------------------

        "result_id": None,

        # ----------------------------------------------------
        # Memory
        # ----------------------------------------------------

        "short_term_memory": None,
    }


def initialize_session_state() -> None:
    """
    Initialize Streamlit session state.
    """

    if "triage_state" not in st.session_state:

        st.session_state.triage_state = (
            create_initial_state()
        )

    if "messages" not in st.session_state:

        st.session_state.messages = []


initialize_session_state()


# ============================================================
# Helpers
# ============================================================

def reset_assessment() -> None:
    """
    Start a new triage assessment while preserving
    authentication context.
    """

    st.session_state.triage_state = (
        create_initial_state()
    )

    st.session_state.messages = []


def logout() -> None:
    """
    Clear authentication and application state.
    """

    keys = [
        "authenticated",
        "user_id",
        "email",
        "roles",
        "patient_id",
        "triage_state",
        "messages",
    ]

    for key in keys:

        st.session_state.pop(
            key,
            None,
        )


def add_message(
    role: str,
    content: str | None,
) -> None:
    """
    Add a message to conversation history.
    """

    if not content:
        return

    st.session_state.messages.append(
        {
            "role": role,
            "content": str(content),
        }
    )


def show_assistant_message(
    content: str | None,
) -> None:
    """
    Render an assistant message.
    """

    if not content:
        return

    with st.chat_message("assistant"):

        st.markdown(content)


# ============================================================
# Role Helpers
# ============================================================

def get_roles() -> list[str]:
    """
    Return normalized user roles.
    """

    return [
        str(role).lower()
        for role in st.session_state.get(
            "roles",
            [],
        )
    ]


def has_role(role: str) -> bool:
    """
    Check whether the authenticated user
    has a specific role.
    """

    return role.lower() in get_roles()


# ============================================================
# Dashboard
# ============================================================

def render_patient_dashboard() -> None:
    """
    Patient dashboard.
    """

    st.subheader("Patient Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "User ID",
            st.session_state.get(
                "user_id",
                "-",
            ),
        )

    with col2:

        st.metric(
            "Patient ID",
            st.session_state.get(
                "patient_id",
                "-",
            ),
        )

    with col3:

        st.metric(
            "Role",
            "Patient",
        )

    st.info(
        "You can start a new medical triage assessment "
        "or continue the current conversation."
    )


def render_doctor_dashboard() -> None:
    """
    Doctor dashboard.
    """

    st.subheader("Doctor Dashboard")

    st.info(
        "Doctor dashboard is available for "
        "patient review, triage results and referrals."
    )

    st.write(
        "Current architecture provides the foundation "
        "for doctor-facing workflows."
    )


def render_hospital_admin_dashboard() -> None:
    """
    Hospital administrator dashboard.
    """

    st.subheader(
        "Hospital Admin Dashboard"
    )

    st.info(
        "Hospital administration features can be "
        "connected to HealthcareOrg and DoctorProfile."
    )


def render_system_admin_dashboard() -> None:
    """
    System administrator dashboard.
    """

    st.subheader(
        "System Admin Dashboard"
    )

    st.info(
        "System administration features can be "
        "connected to UserAccount, Role and AuditLog."
    )


def render_role_dashboard() -> None:
    """
    Render dashboard according to the user's role.
    """

    roles = get_roles()

    if "systemadmin" in roles:

        render_system_admin_dashboard()

        return

    if "hospitaladmin" in roles:

        render_hospital_admin_dashboard()

        return

    if "doctor" in roles:

        render_doctor_dashboard()

        return

    if "patient" in roles:

        render_patient_dashboard()

        return

    st.warning(
        "No supported application role is assigned "
        "to this account."
    )


# ============================================================
# Triage Result Formatter
# ============================================================

def build_triage_response(
    state: dict,
) -> str | None:
    """
    Convert triage state into a user-facing response.
    """

    lines: list[str] = []

    # --------------------------------------------------------
    # Risk
    # --------------------------------------------------------

    if state.get("risk_level"):

        lines.append(
            f"**Risk Level:** "
            f"{state['risk_level']}"
        )

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    if state.get("confidence") is not None:

        confidence = state["confidence"]

        if (
            isinstance(
                confidence,
                float,
            )
            and confidence <= 1
        ):

            confidence = (
                f"{confidence * 100:.0f}%"
            )

        lines.append(
            f"**Confidence:** "
            f"{confidence}"
        )

    # --------------------------------------------------------
    # Red Flags
    # --------------------------------------------------------

    if state.get("red_flags"):

        red_flags = "\n".join(
            f"- {item}"
            for item in state["red_flags"]
        )

        lines.append(
            f"**Red Flags:**\n{red_flags}"
        )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    if state.get("recommendation"):

        lines.append(
            f"**Recommendation:** "
            f"{state['recommendation']}"
        )

    # --------------------------------------------------------
    # Supervisor
    # --------------------------------------------------------

    if state.get("supervisor_status"):

        lines.append(
            f"**Supervisor:** "
            f"{state['supervisor_status']}"
        )

    # --------------------------------------------------------
    # Patient Information
    # --------------------------------------------------------

    patient_info: list[str] = []

    if state.get("age") is not None:

        patient_info.append(
            f"Age: {state['age']}"
        )

    if state.get("symptoms"):

        patient_info.append(
            "Symptoms: "
            + ", ".join(
                state["symptoms"]
            )
        )

    if state.get("duration"):

        patient_info.append(
            f"Duration: {state['duration']}"
        )

    if state.get("severity"):

        patient_info.append(
            f"Severity: {state['severity']}"
        )

    if patient_info:

        lines.append(
            "**Patient Information:**\n"
            + "\n".join(
                f"- {item}"
                for item in patient_info
            )
        )

    if not lines:

        return None

    return "\n\n".join(lines)


# ============================================================
# Header
# ============================================================

st.title("Medical AI Triage")

st.caption(
    "Conversational medical triage prototype"
)


# ============================================================
# Current State
# ============================================================

state = st.session_state.triage_state


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("Account")

    st.write(
        f"**Email:** "
        f"{st.session_state.get('email', '-')}"
    )

    st.write(
        f"**User ID:** "
        f"{st.session_state.get('user_id', '-')}"
    )

    st.write(
        f"**Patient ID:** "
        f"{st.session_state.get('patient_id', '-')}"
    )

    roles = get_roles()

    if roles:

        st.write(
            "**Roles:** "
            + ", ".join(
                role.title()
                for role in roles
            )
        )

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True,
    ):

        logout()

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # Session
    # --------------------------------------------------------

    st.header("Triage Session")

    session_id = state.get(
        "session_id"
    )

    if session_id:

        st.write(
            f"Session ID: {session_id}"
        )

    else:

        st.info(
            "No active session"
        )

    if st.button(
        "Start New Assessment",
        use_container_width=True,
    ):

        reset_assessment()

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # Assessment Status
    # --------------------------------------------------------

    st.header("Assessment Status")

    st.write(
        f"**Intent:** "
        f"{state.get('intent') or 'Pending'}"
    )

    st.write(
        f"**Risk:** "
        f"{state.get('risk_level') or 'Pending'}"
    )

    st.divider()

    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    st.header("Assessment Progress")

    fields = [
        (
            "Age",
            state.get("age") is not None,
        ),
        (
            "Symptoms",
            bool(state.get("symptoms")),
        ),
        (
            "Duration",
            state.get("duration") is not None,
        ),
        (
            "Severity",
            state.get("severity") is not None,
        ),
    ]

    completed = sum(
        1
        for _, done in fields
        if done
    )

    for label, done in fields:

        if done:

            st.write(
                f"✓ {label}"
            )

        else:

            st.write(
                f"○ {label}"
            )

    progress = (
        completed / len(fields)
        if fields
        else 0
    )

    st.progress(progress)

    st.caption(
        f"{completed}/{len(fields)} "
        "information collected"
    )

    st.divider()

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    st.header("Safety")

    st.caption(
        "AI-assisted triage prototype. "
        "Not a replacement for professional medical care."
    )


# ============================================================
# Main Dashboard
# ============================================================

render_role_dashboard()

st.divider()


# ============================================================
# Conversation
# ============================================================

st.subheader("Conversation")


for message in st.session_state.messages:

    role = message.get("role")

    content = message.get("content")

    if not content:
        continue

    with st.chat_message(role):

        st.markdown(content)


# ============================================================
# Chat Input
# ============================================================

user_message = st.chat_input(
    "علائم خود را توضیح دهید یا سؤال خود را بپرسید..."
)


if user_message:

    # --------------------------------------------------------
    # User Message
    # --------------------------------------------------------

    add_message(
        "user",
        user_message,
    )

    with st.chat_message("user"):

        st.markdown(user_message)

    # --------------------------------------------------------
    # Build Graph State
    # --------------------------------------------------------

    current_state = dict(
        st.session_state.triage_state
    )

    current_state["user_message"] = (
        user_message
    )

    current_state["user_id"] = (
        st.session_state.get("user_id")
    )

    current_state["patient_id"] = (
        st.session_state.get("patient_id")
    )

    current_state["user_roles"] = (
        st.session_state.get(
            "roles",
            [],
        )
    )

    # --------------------------------------------------------
    # Authentication Context Validation
    # --------------------------------------------------------

    if has_role("patient"):

        if current_state["patient_id"] is None:

            st.error(
                "Patient authentication context is missing. "
                "Please log out and log in again."
            )

            st.stop()

    # --------------------------------------------------------
    # Run Triage Graph
    # --------------------------------------------------------

    try:

        result = triage_graph.invoke(
            current_state
        )

    except Exception as exc:

        error_message = (
            "خطایی هنگام پردازش درخواست رخ داد.\n\n"
            f"`{type(exc).__name__}: {exc}`"
        )

        add_message(
            "assistant",
            error_message,
        )

        with st.chat_message("assistant"):

            st.error(error_message)

        st.stop()

    # --------------------------------------------------------
    # Persist Application State
    # --------------------------------------------------------

    st.session_state.triage_state = result

    state = result

    # --------------------------------------------------------
    # Response Handling
    # --------------------------------------------------------

    intent = state.get("intent")

    # --------------------------------------------------------
    # General Conversation
    # --------------------------------------------------------

    if intent == "GENERAL":

        response = state.get(
            "assistant_response"
        )

        if not response:

            response = (
                "من اینجا هستم تا در مورد درخواست شما "
                "راهنمایی کنم."
            )

        add_message(
            "assistant",
            response,
        )

        show_assistant_message(
            response
        )

    # --------------------------------------------------------
    # Medical Triage
    # --------------------------------------------------------

    elif intent == "TRIAGE":

        missing = (
            state.get(
                "missing_information"
            )
            or []
        )

        if missing:

            question = state.get(
                "next_question"
            )

            if question:

                add_message(
                    "assistant",
                    question,
                )

                show_assistant_message(
                    question
                )

        else:

            assessment = (
                build_triage_response(
                    state
                )
            )

            if assessment:

                add_message(
                    "assistant",
                    assessment,
                )

                show_assistant_message(
                    assessment
                )

            else:

                display_response = (
                    state.get(
                        "assistant_response"
                    )
                    or state.get(
                        "response"
                    )
                )

                if display_response:

                    add_message(
                        "assistant",
                        display_response,
                    )

                    show_assistant_message(
                        display_response
                    )

    # --------------------------------------------------------
    # Unknown Intent
    # --------------------------------------------------------

    else:

        response = (
            state.get(
                "assistant_response"
            )
            or state.get(
                "response"
            )
            or "لطفاً درخواست خود را توضیح دهید."
        )

        add_message(
            "assistant",
            response,
        )

        show_assistant_message(
            response
        )


# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "Medical AI Triage Prototype — "
    "Rule-based safety baseline + LLM-ready architecture"
)