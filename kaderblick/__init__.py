"""
Kaderblick Dual Camera Control Package

This package provides Python interface for controlling Kaderblick dual camera systems.
"""

__version__ = "0.1.0"
__author__ = "Kaderblick CameraControl Python"

from .camera import Camera, DualCamera
from .config import CameraConfig
from .exceptions import (
    KaderblickError,
    CameraConnectionError,
    CameraOperationError,
    ConfigurationError,
)

__all__ = [
    "Camera",
    "DualCamera",
    "CameraConfig",
    "KaderblickError",
    "CameraConnectionError",
    "CameraOperationError",
    "ConfigurationError",
]
