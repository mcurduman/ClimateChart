class ApiKeyInfo:
    def __init__(
        self,
        user_email: str,
        value: str,
        created_at: str,
    ):
        self.user_email = user_email
        self.value = value
        self.created_at = created_at

    def to_dict(self):
        return {
            "user_email": self.user_email,
            "value": self.value,
            "created_at": self.created_at,
        }
