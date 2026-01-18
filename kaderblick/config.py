"""
Configuration management for Kaderblick cameras.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from .exceptions import ConfigurationError


class CameraConfig:
    """Configuration class for Kaderblick cameras."""

    DEFAULT_CONFIG = {
        "resolution": (1920, 1080),
        "fps": 30,
        "format": "MJPEG",
        "brightness": 50,
        "contrast": 50,
        "saturation": 50,
        "auto_exposure": True,
        "auto_white_balance": True,
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize camera configuration.

        Args:
            config: Optional dictionary with configuration parameters
        """
        self._config = self.DEFAULT_CONFIG.copy()
        if config:
            self._config.update(config)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value

    def update(self, config: Dict[str, Any]) -> None:
        """Update configuration with multiple values."""
        self._config.update(config)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self._config.copy()

    def save(self, filepath: str) -> None:
        """
        Save configuration to JSON file.

        Args:
            filepath: Path to save configuration file
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self._config, f, indent=4)
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")

    @classmethod
    def load(cls, filepath: str) -> 'CameraConfig':
        """
        Load configuration from JSON file.

        Args:
            filepath: Path to configuration file

        Returns:
            CameraConfig instance
        """
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
            return cls(config)
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")

    def __repr__(self) -> str:
        return f"CameraConfig({self._config})"
