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
    # Permission Checks
    # =========================================================

    @staticmethod
    def can_access_patient_data(user) -> bool:
        """
        Determine whether the user may access
        patient-related data.
        """

        return AuthorizationService.has_any_role(
            user,
            [
                AuthorizationService.PATIENT,
                AuthorizationService.DOCTOR,
                AuthorizationService.HOSPITAL_ADMIN,
                AuthorizationService.SYSTEM_ADMIN,
            ],
        )

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