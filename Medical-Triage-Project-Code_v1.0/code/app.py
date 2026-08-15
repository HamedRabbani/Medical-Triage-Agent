import streamlit as st

from workflow.triage_graph import triage_graph


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
# Initial State
# ============================================================

def create_initial_state():
    """
    Create a clean initial workflow state.

    The structure must remain compatible with TriageState.
    """

    return {
        # ----------------------------------------------------
        # Patient / Session
        # ----------------------------------------------------
        "patient_id": 2,
        "session_id": None,

        # ----------------------------------------------------
        # Input
        # ----------------------------------------------------
        "user_message": "",

        # ----------------------------------------------------
        # Patient Information
        # ----------------------------------------------------
        "age": None,
        "symptoms": [],
        "severity": None,
        "duration": None,

        # ----------------------------------------------------
        # Rule-Based Risk Assessment
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
        # LLM Risk Assessment
        # ----------------------------------------------------
        "llm_risk_level": None,
        "llm_confidence": None,
        "llm_red_flags": [],
        "llm_recommendation": None,

        # ----------------------------------------------------
        # Supervisor
        # ----------------------------------------------------
        "supervisor_status": None,

        # ----------------------------------------------------
        # Conversation
        # ----------------------------------------------------
        "conversation_history": [],
        "intent": None,
        "intent_confidence": None,
        "assistant_response": None,

        # ----------------------------------------------------
        # Persistence
        # ----------------------------------------------------
        "result_id": None,

        # ----------------------------------------------------
        # Memory
        # ----------------------------------------------------
        "short_term_memory": None,
    }


# ============================================================
# Streamlit Session Initialization
# ============================================================

if "triage_state" not in st.session_state:
    st.session_state.triage_state = create_initial_state()


if "messages" not in st.session_state:
    st.session_state.messages = []


if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = set()


# ============================================================
# Helper Functions
# ============================================================

def reset_assessment():
    """
    Completely reset the current assessment.
    """

    st.session_state.triage_state = create_initial_state()
    st.session_state.messages = []
    st.session_state.asked_questions = set()


def add_message(role: str, content: str):
    """
    Add a message to the Streamlit UI history.

    Empty messages are ignored.
    """

    if not content:
        return

    content = str(content).strip()

    if not content:
        return

    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
        }
    )


def show_assistant_message(content: str):
    """
    Render an assistant message.
    """

    if not content:
        return

    with st.chat_message("assistant"):
        st.markdown(content)


def normalize_question(question):
    """
    Normalize a question for duplicate detection.
    """

    if not question:
        return ""

    return " ".join(
        str(question)
        .strip()
        .lower()
        .split()
    )


def should_show_question(question):
    """
    Prevent the same question from being displayed repeatedly.
    """

    normalized = normalize_question(question)

    if not normalized:
        return False

    if normalized in st.session_state.asked_questions:
        return False

    st.session_state.asked_questions.add(
        normalized
    )

    return True


def get_progress(state):
    """
    Calculate required triage information progress.
    """

    required_fields = [
        state.get("age"),
        state.get("symptoms"),
        state.get("duration"),
        state.get("severity"),
    ]

    completed = sum(
        bool(value)
        for value in required_fields
    )

    total = len(required_fields)

    return completed, total


def is_triage_complete(state):
    """
    Determine whether all required information exists.
    """

    completed, total = get_progress(state)

    return completed == total


def build_triage_response(state):
    """
    Build the final triage assessment message.
    """

    risk = state.get("risk_level")
    confidence = state.get("confidence")
    supervisor = state.get("supervisor_status")
    recommendation = state.get("recommendation")

    lines = []

    if risk:
        lines.append(
            f"**Risk Level:** {risk}"
        )

    if confidence is not None:
        try:
            confidence_value = float(confidence)

            # Support both:
            # 0.85 -> 85%
            # 85   -> 85%
            if confidence_value <= 1:
                confidence_value *= 100

            lines.append(
                f"**Confidence:** {confidence_value:.0f}%"
            )

        except (TypeError, ValueError):
            lines.append(
                f"**Confidence:** {confidence}"
            )

    if supervisor:
        formatted_supervisor = (
            str(supervisor)
            .replace("_", " ")
            .title()
        )

        lines.append(
            f"**Supervisor:** {formatted_supervisor}"
        )

    if recommendation:
        lines.append(
            f"**Recommendation:** {recommendation}"
        )

    if not lines:
        return None

    return "\n\n".join(lines)


def build_collected_data(state):
    """
    Build collected patient information.
    """

    age = state.get("age")
    symptoms = state.get("symptoms") or []
    duration = state.get("duration")
    severity = state.get("severity")

    return {
        "age": (
            str(age)
            if age is not None
            else "Not provided"
        ),
        "symptoms": (
            ", ".join(symptoms)
            if symptoms
            else "None"
        ),
        "duration": (
            str(duration)
            if duration
            else "Not provided"
        ),
        "severity": (
            str(severity)
            if severity
            else "Not provided"
        ),
    }


def display_question(question):
    """
    Display a new question only once.
    """

    if not question:
        return

    if not should_show_question(question):
        return

    add_message(
        "assistant",
        question,
    )

    show_assistant_message(
        question
    )


def display_general_response(response):
    """
    Display general conversation response.
    """

    if not response:
        response = (
            "من اینجا هستم تا کمکتان کنم. "
            "چطور می‌توانم به شما کمک کنم؟"
        )

    add_message(
        "assistant",
        response,
    )

    show_assistant_message(
        response
    )


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

    st.header("Session")

    session_id = state.get("session_id")

    if session_id is None:
        st.info("No active session")
    else:
        st.write(
            f"**Session ID:** {session_id}"
        )

    st.divider()

    if st.button(
        "شروع ارزیابی جدید / New Assessment",
        use_container_width=True,
    ):
        reset_assessment()
        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # Current Assessment
    # --------------------------------------------------------

    st.header("Current Assessment")

    intent = state.get("intent")

    if intent:
        st.write(
            f"**Intent:** {intent}"
        )
    else:
        st.write(
            "**Intent:** Pending"
        )

    risk = state.get("risk_level")

    if risk:
        st.write(
            f"**Risk:** {risk}"
        )
    else:
        st.write(
            "**Risk:** Pending"
        )

    st.divider()

    # --------------------------------------------------------
    # Collected Data
    # --------------------------------------------------------

    st.header("Collected Data")

    collected = build_collected_data(
        state
    )

    st.write(
        f"**Age:** {collected['age']}"
    )

    st.write(
        f"**Symptoms:** {collected['symptoms']}"
    )

    st.write(
        f"**Duration:** {collected['duration']}"
    )

    st.write(
        f"**Severity:** {collected['severity']}"
    )

    completed, total = get_progress(
        state
    )

    st.write(
        f"**Information:** {completed}/{total}"
    )

    st.progress(
        completed / total
        if total
        else 0
    )

    st.divider()

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    st.header("Safety")

    st.caption(
        "This is an AI-assisted triage prototype "
        "and is not a replacement for professional "
        "medical care."
    )


# ============================================================
# Conversation
# ============================================================

st.subheader("Conversation")


for message in st.session_state.messages:

    role = message.get("role")
    content = message.get("content")

    if not content:
        continue

    if role not in ("user", "assistant"):
        continue

    with st.chat_message(role):
        st.markdown(content)


# ============================================================
# User Input
# ============================================================

user_message = st.chat_input(
    "علائم خود را توضیح دهید یا به سؤال پاسخ دهید..."
)


if user_message:

    user_message = user_message.strip()

    if not user_message:
        st.stop()

    # --------------------------------------------------------
    # Show User Message
    # --------------------------------------------------------

    add_message(
        "user",
        user_message,
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    # --------------------------------------------------------
    # Prepare State
    # --------------------------------------------------------

    current_state = dict(
        st.session_state.triage_state
    )

    current_state["user_message"] = (
        user_message
    )

    # --------------------------------------------------------
    # Invoke LangGraph
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
    # Persist State
    # --------------------------------------------------------

    st.session_state.triage_state = result

    state = result

    # --------------------------------------------------------
    # Intent
    # --------------------------------------------------------

    intent = state.get("intent")

    # ========================================================
    # GENERAL CONVERSATION
    # ========================================================

    if intent == "GENERAL":

        response = state.get(
            "assistant_response"
        )

        display_general_response(
            response
        )

    # ========================================================
    # TRIAGE
    # ========================================================

    elif intent == "TRIAGE":

        missing_information = (
            state.get(
                "missing_information"
            )
            or []
        )

        # ----------------------------------------------------
        # Incomplete Assessment
        # ----------------------------------------------------

        if missing_information:

            question = state.get(
                "next_question"
            )

            display_question(
                question
            )

        # ----------------------------------------------------
        # Complete Assessment
        # ----------------------------------------------------

        else:

            response = (
                state.get(
                    "assistant_response"
                )
            )

            if response:

                add_message(
                    "assistant",
                    response,
                )

                show_assistant_message(
                    response
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

    # ========================================================
    # Unknown Intent
    # ========================================================

    else:

        fallback = (
            "لطفاً درخواست یا علائم خود را "
            "توضیح دهید.\n\n"
            "Please describe your request or symptoms."
        )

        add_message(
            "assistant",
            fallback,
        )

        show_assistant_message(
            fallback
        )


# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "Medical AI Triage Prototype — "
    "Rule-based safety baseline + LLM architecture"
)