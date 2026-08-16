from application.auth.password_service import (
    PasswordService,
)

from application.contracts.auth.login_request import (
    LoginRequest,
)

from application.contracts.auth.login_response import (
    LoginResponse,
)

from infrastructure.auth.auth_repository import (
    AuthRepository,
)


class AuthService:
    """
    Application service responsible for authentication.

    Responsibilities:
    - Validate login credentials
    - Verify password
    - Check account status
    - Resolve user role
    - Resolve patient/doctor context
    """

    def __init__(
        self,
        auth_repository: AuthRepository,
        password_service: type[PasswordService] = PasswordService,
    ):
        self.auth_repository = auth_repository
        self.password_service = password_service

    def login(
        self,
        request: LoginRequest,
    ) -> LoginResponse:

        email = request.email.strip().lower()

        user = self.auth_repository.get_user_by_email(
            email
        )

        # -------------------------------------------------
        # Do not reveal whether the email exists.
        # -------------------------------------------------

        if user is None:
            return LoginResponse(
                success=False,
                message="Invalid email or password.",
            )

        # -------------------------------------------------
        # Account status
        # -------------------------------------------------

        if user.status != "Active":
            return LoginResponse(
                success=False,
                message="Account is not active.",
            )

        # -------------------------------------------------
        # Password verification
        # -------------------------------------------------

        password_valid = (
            self.password_service.verify_password(
                request.password,
                user.password_hash,
            )
        )

        if not password_valid:
            return LoginResponse(
                success=False,
                message="Invalid email or password.",
            )

        # -------------------------------------------------
        # Role resolution
        # -------------------------------------------------

        role_name = None

        if user.user_roles:

            roles = [
                assignment.role.role_name
                for assignment in user.user_roles
                if assignment.role is not None
            ]

            if roles:
                role_name = roles[0]

        # -------------------------------------------------
        # Patient / Doctor context
        # -------------------------------------------------

        patient_id = None
        doctor_id = None

        if user.patient_profile is not None:
            patient_id = (
                user.patient_profile.patient_id
            )

        if user.doctor_profile is not None:
            doctor_id = (
                user.doctor_profile.doctor_id
            )

        # -------------------------------------------------
        # Successful authentication
        # -------------------------------------------------

        return LoginResponse(
            success=True,
            user_id=user.user_id,
            email=user.email,
            role=role_name,
            patient_id=patient_id,
            doctor_id=doctor_id,
            message="Authentication successful.",
        )