class DomainError(Exception):
    pass

class AccountNotFound(DomainError):
    pass

class InsufficientFunds(DomainError):
    pass

class AccountClosed(DomainError):
    pass