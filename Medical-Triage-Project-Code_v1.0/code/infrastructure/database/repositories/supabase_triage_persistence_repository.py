from datetime import UTC, datetime

from application.ports.triage_persistence_port import (
    TriagePersistencePort,
)


class SupabaseTriagePersistenceRepository(
    TriagePersistencePort
):
    """Supabase implementation of triage persistence."""

    def __init__(
        self,
        client,
        patient_table: str = "PatientProfile",
        session_table: str = "TriageSession",
        message_table: str = "ConversationMsg",
        result_table: str = "TriageResult",
    ):
        self.client = client
        self.patient_table = patient_table
        self.session_table = session_table
        self.message_table = message_table
        self.result_table = result_table

    # =========================================================
    # Patient
    # =========================================================

    def patient_exists(
        self,
        patient_id: int,
    ) -> bool:

        response = (
            self.client
            .table(self.patient_table)
            .select("PatientId")
            .eq("PatientId", patient_id)
            .limit(1)
            .execute()
        )

        return bool(response.data)

    # =========================================================
    # Session
    # =========================================================

    def create_session(
        self,
        patient_id: int,
    ):

        response = (
            self.client
            .table(self.session_table)
            .insert(
                {
                    "PatientId": patient_id,
                    "StartTime": (
                        datetime.now(UTC).isoformat()
                    ),
                    "Status": "Active",
                }
            )
            .execute()
        )

        rows = response.data or []

        if not rows:
            raise RuntimeError(
                "Supabase did not return the created session."
            )

        return _SessionRecord(
            session_id=rows[0]["SessionId"],
            patient_id=rows[0]["PatientId"],
            status=rows[0]["Status"],
        )

    def get_session(
        self,
        session_id: int,
    ):

        response = (
            self.client
            .table(self.session_table)
            .select(
                "SessionId,PatientId,StartTime,EndTime,Status"
            )
            .eq("SessionId", session_id)
            .limit(1)
            .execute()
        )

        rows = response.data or []

        if not rows:
            return None

        row = rows[0]

        return _SessionRecord(
            session_id=row["SessionId"],
            patient_id=row["PatientId"],
            status=row["Status"],
        )

    # =========================================================
    # Message
    # =========================================================

    def add_message(
        self,
        session_id: int,
        sender_type: str,
        content: str,
    ):

        response = (
            self.client
            .table(self.message_table)
            .insert(
                {
                    "SessionId": session_id,
                    "SenderType": sender_type,
                    "Content": content,
                    "Timestamp": (
                        datetime.now(UTC).isoformat()
                    ),
                }
            )
            .execute()
        )

        rows = response.data or []

        if not rows:
            raise RuntimeError(
                "Supabase did not return the created message."
            )

        return _MessageRecord(
            message_id=rows[0]["MessageId"],
            session_id=rows[0]["SessionId"],
            sender_type=rows[0]["SenderType"],
            content=rows[0]["Content"],
        )

    # =========================================================
    # Result
    # =========================================================

    def add_result(
        self,
        session_id: int,
        risk_level: str,
        confidence_score: float,
        recommendation: str,
    ):

        response = (
            self.client
            .table(self.result_table)
            .insert(
                {
                    "SessionId": session_id,
                    "RiskLevel": risk_level,
                    "ConfidenceScore": confidence_score,
                    "Recommendation": recommendation,
                    "CreatedAt": (
                        datetime.now(UTC).isoformat()
                    ),
                }
            )
            .execute()
        )

        rows = response.data or []

        if not rows:
            raise RuntimeError(
                "Supabase did not return the created result."
            )

        return _ResultRecord(
            result_id=rows[0]["ResultId"],
            session_id=rows[0]["SessionId"],
            risk_level=rows[0]["RiskLevel"],
            confidence_score=rows[0]["ConfidenceScore"],
            recommendation=rows[0]["Recommendation"],
        )

    # =========================================================
    # Transaction
    # =========================================================

    def commit(self) -> None:
        # Supabase REST operations are submitted immediately.
        return None

    def rollback(self) -> None:
        # No client-side transaction is opened by this adapter.
        return None


class _SessionRecord:
    def __init__(
        self,
        session_id: int,
        patient_id: int,
        status: str,
    ):
        self.session_id = session_id
        self.patient_id = patient_id
        self.status = status


class _MessageRecord:
    def __init__(
        self,
        message_id: int,
        session_id: int,
        sender_type: str,
        content: str,
    ):
        self.message_id = message_id
        self.session_id = session_id
        self.sender_type = sender_type
        self.content = content


class _ResultRecord:
    def __init__(
        self,
        result_id: int,
        session_id: int,
        risk_level: str,
        confidence_score: float,
        recommendation: str,
    ):
        self.result_id = result_id
        self.session_id = session_id
        self.risk_level = risk_level
        self.confidence_score = confidence_score
        self.recommendation = recommendation