class IsengardError(Exception):
    pass


class IsengardStateError(Exception):
    pass


class IsengardDefinitionError(IsengardError):
    pass


class IsengardConsistencyError(IsengardError):
    pass


class IsengardRunError(IsengardError):
    pass
