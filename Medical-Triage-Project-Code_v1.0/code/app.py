import streamlit as st

from workflow.triage_graph import triage_graph


st.set_page_config(
    page_title="Medical AI Triage",
    page_icon="🏥",
)

st.title("Medical AI Triage")
st.success("Success")


def create_initial_state():

    return {
    "user_message": "",
    "age": None,
    "symptoms": [],
    "severity": None,
    "duration": None,
    "red_flags": [],
    "missing_information": [],
    "next_question": None,
    "risk_level": None,
    "confidence": None,
    "supervisor_status": None,
    "recommendation": None,
    "patient_id": 2,
    "session_id": None,
    "conversation_history": [],
}


if "triage_state" not in st.session_state:
    st.session_state.triage_state = create_initial_state()


if "messages" not in st.session_state:
    st.session_state.messages = []


if st.button(
    "شروع ارزیابی جدید / Start New Assessment"
):

    st.session_state.triage_state = (
        create_initial_state()
    )

    st.session_state.messages = []

    st.rerun()


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


user_message = st.chat_input(
    "علائم خود را توضیح دهید / Describe your symptoms..."
)


if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message,
    })

    with st.chat_message("user"):
        st.write(user_message)

    current_state = (
        st.session_state.triage_state.copy()
    )

    current_state["user_message"] = user_message

    result = triage_graph.invoke(
    current_state
    )

    # st.write("DEBUG - Conversation History")

    # st.json(
    #     result.get(
    #         "conversation_history",
    #         []
    #     )
    # )

    
    st.session_state.triage_state = result

    # Incomplete information
    if result.get("missing_information"):

        question = result.get(
            "next_question"
        )

        if question:

            st.session_state.messages.append({
                "role": "assistant",
                "content": question,
            })

            with st.chat_message("assistant"):
                st.write(question)

    # Complete information
    else:

        risk = result.get("risk_level")
        confidence = result.get("confidence")
        supervisor = result.get(
            "supervisor_status"
        )
        recommendation = result.get(
            "recommendation"
        )

        response = (
            f"**Risk Level:** {risk}\n\n"
            f"**Confidence:** "
            f"{confidence * 100:.0f}%\n\n"
            f"**Supervisor:** {supervisor}\n\n"
            f"**Recommendation:** "
            f"{recommendation}"
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
        })

        with st.chat_message("assistant"):
            st.markdown(response)