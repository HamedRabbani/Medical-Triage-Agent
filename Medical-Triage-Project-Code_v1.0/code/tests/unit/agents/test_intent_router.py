import pytest

from agents.conversation_agent import (
    _detect_intent_from_message,
)

def base_state(**overrides):
    state = {
        "intent": None,
        "missing_information": [],
        "next_question": None,
        "symptoms": [],
        "age": None,
        "duration": None,
        "severity": None,
    }

    state.update(overrides)

    return state


# ============================================================
# GENERAL
# ============================================================

def test_greeting_is_general():

    state = base_state()

    intent, confidence = _detect_intent_from_message(
        state,
        "سلام"
    )

    assert intent == "GENERAL"
    assert confidence > 0


def test_casual_question_is_general():

    state = base_state()

    intent, _ = _detect_intent_from_message(
        state,
        "امروز هوا چطوره؟"
    )

    assert intent == "GENERAL"


# ============================================================
# TRIAGE
# ============================================================

def test_symptom_starts_triage():

    state = base_state()

    intent, confidence = _detect_intent_from_message(
        state,
        "سرم درد می‌کنه"
    )

    assert intent == "TRIAGE"
    assert confidence > 0


def test_age_starts_triage():

    state = base_state()

    intent, _ = _detect_intent_from_message(
        state,
        "من ۳۰ سالمه"
    )

    assert intent == "TRIAGE"


def test_duration_starts_triage():

    state = base_state()

    intent, _ = _detect_intent_from_message(
        state,
        "سه روزه اینطوری شدم"
    )

    assert intent == "TRIAGE"


def test_severity_starts_triage():

    state = base_state()

    intent, _ = _detect_intent_from_message(
        state,
        "دردم خیلی شدیده"
    )

    assert intent == "TRIAGE"


# ============================================================
# ACTIVE TRIAGE
# ============================================================

def test_active_triage_keeps_triage():

    state = base_state(
        missing_information=["age"]
    )

    intent, confidence = _detect_intent_from_message(
        state,
        "۳۰ سالمه"
    )

    assert intent == "TRIAGE"
    assert confidence == 1.0


def test_next_question_keeps_triage():

    state = base_state(
        next_question="دردتان از چه زمانی شروع شده؟"
    )

    intent, _ = _detect_intent_from_message(
        state,
        "از دیروز"
    )

    assert intent == "TRIAGE"


# ============================================================
# PROFILE
# ============================================================

def test_profile_request_is_profile():

    state = base_state()

    intent, confidence = _detect_intent_from_message(
        state,
        "اطلاعات من رو نشون بده"
    )

    assert intent == "PROFILE"
    assert confidence == 1.0


def test_my_age_is_profile_request():

    state = base_state()

    intent, _ = _detect_intent_from_message(
        state,
        "سن من چنده؟"
    )

    assert intent == "PROFILE"


def test_profile_has_priority_over_active_triage():

    state = base_state(
        missing_information=["age"]
    )

    intent, _ = _detect_intent_from_message(
        state,
        "پروفایل من رو نشون بده"
    )

    assert intent == "PROFILE"