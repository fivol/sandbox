class CPABaseException(UserWarning):
    """Base class for _celery-pool-asyncio exceptions"""


class SoftRevoked(CPABaseException):
    """Send it from pool to tracer"""
