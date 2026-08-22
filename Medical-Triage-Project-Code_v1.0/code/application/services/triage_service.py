from application.ports.triage_persistence_port import (
    TriagePersistencePort,
)


class TriageService:
    """Application service for triage use cases."""

    def __init__(
        self,
        persistence: TriagePersistencePort,
    ):
        self.persistence = persistence

    def start_session(
        self,
        patient_id: int,
    ):
        """Create a new triage session."""

        if not self.persistence.patient_exists(
            patient_id
        ):
            raise ValueError(
                f"Patient {patient_id} does not exist."
            )

        return self.persistence.create_session(
            patient_id
        )

    def add_message(
        self,
        session_id: int,
        sender_type: str,
        content: str,
    ):
        """Add a message to an existing triage session."""

        triage_session = self.persistence.get_session(
            session_id
        )

        if triage_session is None:
            raise ValueError(
                f"Triage session {session_id} does not exist."
            )

        return self.persistence.add_message(
            session_id=session_id,
            sender_type=sender_type,
            content=content,
        )

    def save_result(
        self,
        session_id: int,
        risk_level: str,
        confidence_score: float,
        recommendation: str,
    ):
        """Persist a triage result."""

        triage_session = self.persistence.get_session(
            session_id
        )

        if triage_session is None:
            raise ValueError(
                f"Triage session {session_id} does not exist."
            )

        return self.persistence.add_result(
            session_id=session_id,
            risk_level=risk_level,
            confidence_score=confidence_score,
            recommendation=recommendation,
        )

    def process_triage(
        self,
        patient_id: int,
        content: str,
        risk_level: str,
        confidence_score: float,
        recommendation: str,
        session_id: int | None = None,
    ):
        """Process triage using a new or existing session."""

        try:
            # -------------------------------------------------
            # Create new session
            # -------------------------------------------------

            if session_id is None:

                session = self.start_session(
                    patient_id
                )

                session_id = session.session_id

            # -------------------------------------------------
            # Verify existing session
            # -------------------------------------------------

            else:

                session = self.persistence.get_session(
                    session_id
                )

                if session is None:
                    raise ValueError(
                        f"Triage session "
                        f"{session_id} does not exist."
                    )

                if session.patient_id != patient_id:
                    raise ValueError(
                        "Session does not belong "
                        "to the specified patient."
                    )

            # -------------------------------------------------
            # Save result
            # -------------------------------------------------

            result = self.save_result(
                session_id=session_id,
                risk_level=risk_level,
                confidence_score=confidence_score,
                recommendation=recommendation,
            )

            # -------------------------------------------------
            # Commit
            # -------------------------------------------------

            self.persistence.commit()

            return result

        except Exception:
            self.persistence.rollback()
            raise