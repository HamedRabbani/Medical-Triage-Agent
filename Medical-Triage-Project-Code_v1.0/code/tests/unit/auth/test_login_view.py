from unittest.mock import MagicMock, patch

import streamlit as st

from presentation.auth.login_view import render_login


def setup_function():
    """
    Reset Streamlit session state before each test.
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def test_render_login_returns_false_when_form_not_submitted():
    """
    Login form should not authenticate the user
    when it has not been submitted.
    """

    with patch(
        "presentation.auth.login_view.st.form_submit_button",
        return_value=False,
    ):
        result = render_login()

    assert result is False
    assert "authenticated" not in st.session_state


def test_render_login_rejects_empty_credentials():
    """
    Empty credentials must not reach LoginService.
    """

    with patch(
        "presentation.auth.login_view.st.text_input",
        side_effect=["", ""],
    ), patch(
        "presentation.auth.login_view.st.form_submit_button",
        return_value=True,
    ), patch(
        "presentation.auth.login_view.create_login_service"
    ) as create_service:

        result = render_login()

    assert result is False

    create_service.assert_not_called()

    assert "authenticated" not in st.session_state


def test_render_login_rejects_invalid_credentials():
    """
    Invalid credentials must not authenticate the user.
    """

    mock_login_service = MagicMock()

    mock_login_service.login.return_value = MagicMock(
        success=False,
        error="Invalid email or password.",
    )

    mock_session = MagicMock()

    with patch(
        "presentation.auth.login_view.st.text_input",
        side_effect=[
            "test@example.com",
            "wrong-password",
        ],
    ), patch(
        "presentation.auth.login_view.st.form_submit_button",
        return_value=True,
    ), patch(
        "presentation.auth.login_view.create_login_service",
        return_value=(
            mock_login_service,
            mock_session,
        ),
    ), patch(
        "presentation.auth.login_view.st.rerun"
    ):

        result = render_login()

    assert result is False

    mock_login_service.login.assert_called_once_with(
        email="test@example.com",
        password="wrong-password",
    )

    mock_session.close.assert_called_once()

    assert "authenticated" not in st.session_state


def test_render_login_authenticates_valid_user():
    """
    Successful authentication must create
    the authenticated session state.
    """

    mock_login_service = MagicMock()

    mock_login_service.login.return_value = MagicMock(
        success=True,
        user_id=10,
        email="doctor@example.com",
        roles=("Doctor",),
        error=None,
    )

    mock_session = MagicMock()

    with patch(
        "presentation.auth.login_view.st.text_input",
        side_effect=[
            "doctor@example.com",
            "correct-password",
        ],
    ), patch(
        "presentation.auth.login_view.st.form_submit_button",
        return_value=True,
    ), patch(
        "presentation.auth.login_view.create_login_service",
        return_value=(
            mock_login_service,
            mock_session,
        ),
    ), patch(
        "presentation.auth.login_view.st.rerun"
    ):

        result = render_login()

    assert result is not False

    mock_login_service.login.assert_called_once_with(
        email="doctor@example.com",
        password="correct-password",
    )

    mock_session.close.assert_called_once()

    assert st.session_state.authenticated is True
    assert st.session_state.user_id == 10
    assert st.session_state.user_email == "doctor@example.com"
    assert st.session_state.user_roles == ("Doctor",)