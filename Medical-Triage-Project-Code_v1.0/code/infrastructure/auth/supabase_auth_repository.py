from application.ports.auth_port import AuthUser


class SupabaseAuthRepository:
    """Supabase implementation of AuthPort."""

    def __init__(self, client):
        self.client = client

    def get_user_by_email(
        self,
        email: str,
    ) -> AuthUser | None:

        user_response = (
            self.client
            .table("UserAccount")
            .select(
                "UserId,Email,PasswordHash,Status"
            )
            .eq("Email", email)
            .limit(1)
            .execute()
        )

        users = user_response.data or []

        if not users:
            return None

        user = users[0]

        role_response = (
            self.client
            .table("UserRole")
            .select(
                "Role(RoleName)"
            )
            .eq(
                "UserId",
                user["UserId"],
            )
            .execute()
        )

        role_rows = (
            role_response.data or []
        )

        roles: list[str] = []

        for row in role_rows:

            role = row.get("Role")

            if isinstance(role, dict):

                role_name = role.get(
                    "RoleName"
                )

                if role_name:
                    roles.append(
                        str(role_name)
                    )

        return AuthUser(
            user_id=user["UserId"],
            email=user["Email"],
            password_hash=user["PasswordHash"],
            status=user["Status"],
            roles=tuple(
                sorted(set(roles))
            ),
        )