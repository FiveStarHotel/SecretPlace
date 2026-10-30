class AppError(Exception):
    status_code = 400
    detail = "Bad Request"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class SecretNotFoundError(AppError):
    status_code = 404
    detail = "Secret wasn't found"


class UsernameOccupiedError(AppError):
    status_code = 409
    detail = "Username is occupied"


class CredentialsError(AppError):
    status_code = 401
    detail = "Invalid username or password"


class InvalidAccessTokenError(AppError):
    status_code = 401
    detail = "Invalid access token"


class InvalidRefreshTokenError(AppError):
    status_code = 401
    detail = "Invalid refresh token"


class InactiveUserError(AppError):
    status_code = 403
    detail = "User is inactive"
