import streamlit as st

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

    if not render_login():
        st.stop()



# ============================================================
# Initial State
# ============================================================

def create_initial_state():

    return {

        # Authentication Context

        "user_id": st.session_state.get(
            "user_id"
        ),

        "patient_id": st.session_state.get(
            "patient_id"
        ),

        "user_roles": st.session_state.get(
            "roles",
            []
        ),


        # Session

        "session_id": None,


        # Input

        "user_message": "",


        # Patient Data

        "age": None,

        "symptoms": [],

        "duration": None,

        "severity": None,


        # Risk

        "red_flags": [],

        "risk_level": None,

        "confidence": None,

        "recommendation": None,


        # Planner

        "missing_information": [],

        "next_question": None,


        # Conversation

        "conversation_history": [],

        "intent": None,

        "intent_confidence": None,

        "assistant_response": None,

        "response": None,


        # Supervisor

        "supervisor_status": None,


        # Persistence

        "result_id": None,


        # Memory

        "short_term_memory": None,
    }



# ============================================================
# Session Initialization
# ============================================================

if "triage_state" not in st.session_state:

    st.session_state.triage_state = (
        create_initial_state()
    )


if "messages" not in st.session_state:

    st.session_state.messages = []



# ============================================================
# Helpers
# ============================================================

def reset_assessment():

    st.session_state.triage_state = (
        create_initial_state()
    )

    st.session_state.messages = []



def logout():

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
    role,
    content,
):

    if not content:
        return


    st.session_state.messages.append(
        {
            "role": role,
            "content": str(content),
        }
    )



def show_assistant_message(
    content,
):

    if content:

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                content
            )



def display_general_response(
    response,
):

    if not response:

        response = (
            "من اینجا هستم تا کمک کنم."
        )


    add_message(
        "assistant",
        response,
    )


    show_assistant_message(
        response
    )



def display_question(
    question,
):

    if not question:
        return


    add_message(
        "assistant",
        question,
    )


    show_assistant_message(
        question
    )



# ============================================================
# Triage Result Formatter
# ============================================================

def build_triage_response(state):

    lines = []


    # -------------------------
    # Risk
    # -------------------------

    if state.get("risk_level"):

        lines.append(
            f"**Risk Level:** "
            f"{state['risk_level']}"
        )


    if state.get("confidence") is not None:

        confidence = state["confidence"]


        if (
            isinstance(confidence, float)
            and confidence <= 1
        ):

            confidence = (
                f"{confidence * 100:.0f}%"
            )


        lines.append(
            f"**Confidence:** "
            f"{confidence}"
        )



    # -------------------------
    # Red Flags
    # -------------------------

    if state.get("red_flags"):

        lines.append(
            "**Red Flags:**\n"
            +
            "\n".join(
                [
                    f"- {item}"
                    for item in state["red_flags"]
                ]
            )
        )



    # -------------------------
    # Recommendation
    # -------------------------

    if state.get("recommendation"):

        lines.append(
            f"**Recommendation:** "
            f"{state['recommendation']}"
        )



    # -------------------------
    # Supervisor
    # -------------------------

    if state.get("supervisor_status"):

        lines.append(
            f"**Supervisor:** "
            f"{state['supervisor_status']}"
        )



    # -------------------------
    # Patient Summary
    # -------------------------

    patient_info = []


    if state.get("age") is not None:

        patient_info.append(
            f"Age: {state['age']}"
        )


    if state.get("symptoms"):

        patient_info.append(
            "Symptoms: "
            +
            ", ".join(
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
            +
            "\n".join(
                [
                    f"- {item}"
                    for item in patient_info
                ]
            )
        )



    if not lines:

        return None


    return "\n\n".join(lines)

# ============================================================
# Header
# ============================================================

st.title(
    "Medical AI Triage"
)

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


    st.header(
        "User"
    )


    st.write(
        f"**Email:** "
        f"{st.session_state.get('email')}"
    )


    st.write(
        f"**User ID:** "
        f"{st.session_state.get('user_id')}"
    )


    st.write(
        f"**Patient ID:** "
        f"{st.session_state.get('patient_id')}"
    )


    roles = st.session_state.get(
        "roles",
        []
    )


    if roles:

        st.write(
            "**Roles:** "
            +
            ", ".join(
                [
                    str(role).title()
                    for role in roles
                ]
            )
        )



    if st.button(
        "Logout",
        use_container_width=True,
    ):

        logout()

        st.rerun()



    st.divider()



    # ========================================================
    # Session
    # ========================================================

    st.header(
        "Session"
    )


    if state.get("session_id"):

        st.write(
            f"Session ID: "
            f"{state['session_id']}"
        )

    else:

        st.info(
            "No active session"
        )



    st.divider()



    if st.button(
        "شروع ارزیابی جدید",
        use_container_width=True,
    ):

        reset_assessment()

        st.rerun()



    st.divider()



    # ========================================================
    # Current Assessment
    # ========================================================

    st.header(
        "Current Assessment"
    )


    st.write(
        f"Intent: "
        f"{state.get('intent') or 'Pending'}"
    )


    st.write(
        f"Risk: "
        f"{state.get('risk_level') or 'Pending'}"
    )



    # ========================================================
    # Assessment Progress
    # ========================================================

    st.divider()


    st.header(
        "Assessment Progress"
    )


    fields = [

        (
            "Age",
            state.get("age") is not None
        ),

        (
            "Symptoms",
            bool(state.get("symptoms"))
        ),

        (
            "Duration",
            state.get("duration") is not None
        ),

        (
            "Severity",
            state.get("severity") is not None
        ),

    ]


    completed = 0


    for label, done in fields:


        if done:

            st.write(
                f"✅ {label}"
            )

            completed += 1


        else:

            st.write(
                f"⬜ {label}"
            )



    progress = (
        completed /
        len(fields)
    )


    st.progress(
        progress
    )


    st.caption(
        f"{completed}/{len(fields)} "
        "information collected"
    )



    st.divider()



    # ========================================================
    # Safety
    # ========================================================

    st.header(
        "Safety"
    )


    st.caption(
        "AI-assisted triage prototype. "
        "Not a replacement for professional medical care."
    )





# ============================================================
# Conversation History
# ============================================================

st.subheader(
    "Conversation"
)



for message in st.session_state.messages:


    role = message.get(
        "role"
    )


    content = message.get(
        "content"
    )


    if not content:
        continue


    with st.chat_message(
        role
    ):

        st.markdown(
            content
        )





# ============================================================
# Chat Input
# ============================================================

user_message = st.chat_input(
    "علائم خود را توضیح دهید یا سؤال خود را بپرسید..."
)



if user_message:


    add_message(
        "user",
        user_message,
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_message
        )



    current_state = dict(
        st.session_state.triage_state
    )


    current_state["user_message"] = (
        user_message
    )


    current_state["user_id"] = (
        st.session_state.get(
            "user_id"
        )
    )


    current_state["patient_id"] = (
        st.session_state.get(
            "patient_id"
        )
    )


    current_state["user_roles"] = (
        st.session_state.get(
            "roles",
            []
        )
    )



    # ========================================================
    # Run Graph
    # ========================================================

    try:


        result = triage_graph.invoke(
            current_state
        )


    except Exception as exc:


        error = (
            "خطایی هنگام پردازش درخواست رخ داد.\n\n"
            f"`{type(exc).__name__}: {exc}`"
        )


        add_message(
            "assistant",
            error,
        )


        with st.chat_message(
            "assistant"
        ):

            st.error(
                error
            )


        st.stop()



    # ========================================================
    # Save State
    # ========================================================

    st.session_state.triage_state = result

    state = result



    # ========================================================
    # Response Handling
    # ========================================================

    intent = state.get(
        "intent"
    )


    if intent == "GENERAL":


        display_general_response(
            state.get(
                "assistant_response"
            )
        )



    elif intent == "TRIAGE":


        missing = (
            state.get(
                "missing_information"
            )
            or []
        )


        if missing:


            display_question(
                state.get(
                    "next_question"
                )
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


        display_general_response(
            "لطفاً درخواست خود را توضیح دهید."
        )





# ============================================================
# Footer
# ============================================================

st.divider()


st.caption(
    "Medical AI Triage Prototype — "
    "Rule-based safety baseline + LLM architecture"
)