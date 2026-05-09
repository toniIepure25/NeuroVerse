from __future__ import annotations


class NeuroVerseError(Exception):
    """Base exception for NeuroVerse."""


class SessionNotFoundError(NeuroVerseError):
    """Raised when a requested session does not exist."""


class SessionAlreadyRunningError(NeuroVerseError):
    """Raised when attempting to start a session while one is active."""


class AcquisitionError(NeuroVerseError):
    """Raised on data acquisition failures."""


class ReplayError(NeuroVerseError):
    """Raised on session replay failures."""
