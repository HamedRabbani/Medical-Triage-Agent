class AuthorizationService:
    """
    Application service responsible for role-based authorization.

    Authentication answers:
        "Who is this user?"

    Authorization answers:
        "Is this user allowed to perform this action?"
    """

    # =========================================================
    # Role Definitions
    # =========================================================

    PATIENT = "Patient"
    DOCTOR = "Doctor"
    HOSPITAL_ADMIN = "HospitalAdmin"
    SYSTEM_ADMIN = "SystemAdmin"

    # =========================================================
    # Role Checking
    # =========================================================

    @staticmethod
    def has_role(user, role_name: str) -> bool:
        """
        Return True if the user has the requested role.
        """

        if user is None:
            return False

        if not role_name:
            return False

        user_roles = getattr(
            user,
            "user_roles",
            None,
        )

        if not user_roles:
            return False

        for user_role in user_roles:

            role = getattr(
                user_role,
                "role",
                None,
            )

            if role is None:
                continue

            current_role = getattr(
                role,
                "role_name",
                None,
            )

            if current_role == role_name:
                return True

        return False

    # =========================================================
    # Multiple Role Checking
    # =========================================================

    @staticmethod
    def has_any_role(
        user,
        role_names: list[str],
    ) -> bool:
        """
        Return True if the user has at least one
        of the requested roles.
        """

        if not role_names:
            return False

        return any(
            AuthorizationService.has_role(
                user,
                role_name,
            )
            for role_name in role_names
        )

    # =========================================================
    # Patient Data Access
    # =========================================================

    @staticmethod
    def can_access_patient_data(
        user,
        patient_user_id: int | None = None,
        target_patient_user_id: int | None = None,
    ) -> bool:
        """
        Determine whether the user may access
        the requested patient's data.

        Patients may access only their own data.

        Doctors, Hospital Admins, and System Admins
        may access patient data according to their role.
        """

        if user is None:
            return False

        # Patient → own data only
        if AuthorizationService.has_role(
            user,
            AuthorizationService.PATIENT,
        ):
            return (
                patient_user_id is not None
                and target_patient_user_id is not None
                and patient_user_id == target_patient_user_id
            )

        # Staff roles → patient data
        return AuthorizationService.has_any_role(
            user,
            [
                AuthorizationService.DOCTOR,
                AuthorizationService.HOSPITAL_ADMIN,
                AuthorizationService.SYSTEM_ADMIN,
            ],
        )

    # =========================================================
    # Doctor Data Access
    # =========================================================

    @staticmethod
    def can_access_doctor_data(
        user,
        doctor_user_id: int | None = None,
        target_doctor_user_id: int | None = None,
    ) -> bool:
        """
        Determine whether the user may access
        the requested doctor's data.

        Doctors may access only their own data.

        System Admins may access doctor data.
        """

        if user is None:
            return False

        # Doctor → own data only
        if AuthorizationService.has_role(
            user,
            AuthorizationService.DOCTOR,
        ):
            return (
                doctor_user_id is not None
                and target_doctor_user_id is not None
                and doctor_user_id == target_doctor_user_id
            )

        # System Admin → doctor data
        return AuthorizationService.has_role(
            user,
            AuthorizationService.SYSTEM_ADMIN,
        )

    # =========================================================
    # Patient Data Management
    # =========================================================

    @staticmethod
    def can_manage_patient_data(user) -> bool:
        """
        Determine whether the user may create or
        modify patient clinical information.
        """

        return AuthorizationService.has_any_role(
            user,
            [
                AuthorizationService.DOCTOR,
                AuthorizationService.HOSPITAL_ADMIN,
                AuthorizationService.SYSTEM_ADMIN,
            ],
        )

    # =========================================================
    # User Management
    # =========================================================

    @staticmethod
    def can_manage_users(user) -> bool:
        """
        Determine whether the user may manage
        application accounts.
        """

        return AuthorizationService.has_any_role(
            user,
            [
                AuthorizationService.SYSTEM_ADMIN,
            ],
        )

    # =========================================================
    # Role Management
    # =========================================================

    @staticmethod
    def can_manage_roles(user) -> bool:
        """
        Determine whether the user may assign or
        modify application roles.
        """

        return AuthorizationService.has_role(
            user,
            AuthorizationService.SYSTEM_ADMIN,
        )