from pydantic import BaseModel


class LoginResponse(BaseModel):
    success: bool
    user_id: int | None = None
    email: str | None = None
    role: str | None = None
    patient_id: int | None = None
    doctor_id: int | None = None
    message: str