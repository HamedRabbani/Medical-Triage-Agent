from dataclasses import dataclass


@dataclass
class LongTermMemory:

    patient_profile: dict | None

    medical_history: list[dict]

    previous_triage_results: list[dict]