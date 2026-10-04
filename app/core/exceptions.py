class AppException(Exception):
    status_code = 500
    code = 'INTERNAL_SERVER_ERROR'
    message = 'Internal error'
    details = {}

    def __init__(self,
                 message: str | None = None,
                 *,
                 details: dict | None = None
                 ):
        if message:
            self.message = message
        if details:
            self.details = details

        super().__init__(self.message)


class UnauthorizedError(AppException):
    status_code = 401
    code = 'UNAUTHORIZED_ERROR'
    message = ''


class ForbiddenError(AppException):
    status_code = 403
    code = 'FORBIDDEN_ERROR'
    message = ('You do not have permission '
               'to perform this action')


class NotFoundError(AppException):
    status_code = 404
    code = 'NOT_FOUND_ERROR'
    message = 'Resource not found'


class ItemIsExistError(AppException):
    status_code = 409
    code = 'RESOURCE_ALREADY_EXIST_ERROR'
    message = 'Resource already exists'
