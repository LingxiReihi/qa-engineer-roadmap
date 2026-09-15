class AccountError(Exception):

    def __init__(self, user):
        self.user = user
        super().__init__(user)

    def __str__(self) -> str:
        return f"未查询到用户: {self.user}"


class PasswordError(AccountError):
    def __init__(self, user, message):
        self.user = user
        self.message = message
        super().__init__(user)

    def __str__(self) -> str:
        return f"用户{self.user}{self.message}"
