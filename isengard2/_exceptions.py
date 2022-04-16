class IsengardError(Exception):
    pass


class IsengardStateError(Exception):
    pass


class IsengardConsistencyError(IsengardError):
    pass


class IsengardRunError(IsengardError):
    pass


class IsengardUnknownTargetError(IsengardRunError):
    pass


class IsengardDBError(IsengardRunError):
    pass
