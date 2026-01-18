"""
Custom exceptions for Kaderblick camera control.
"""


class KaderblickError(Exception):
    """Base exception for Kaderblick camera control errors."""
    pass


class CameraConnectionError(KaderblickError):
    """Exception raised when camera connection fails."""
    pass


class CameraOperationError(KaderblickError):
    """Exception raised when camera operation fails."""
    pass


class ConfigurationError(KaderblickError):
    """Exception raised when configuration is invalid."""
    pass
