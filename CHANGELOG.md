# Changelog

All notable changes to the Kaderblick Camera Control Python project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-18

### Added
- Initial release of Kaderblick Camera Control Python package
- `Camera` class for controlling individual cameras
  - Open/close camera connections
  - Capture images
  - Record videos
  - Adjust camera settings (resolution, FPS, brightness, contrast, saturation)
  - Context manager support
- `DualCamera` class for controlling two cameras simultaneously
  - Synchronized image capture
  - Synchronized video recording
  - Independent configuration per camera
- `CameraConfig` class for configuration management
  - Default configuration presets
  - Save/load configuration to/from JSON files
  - Runtime configuration updates
- Custom exception classes
  - `KaderblickError` (base exception)
  - `CameraConnectionError` for connection failures
  - `CameraOperationError` for operation failures
  - `ConfigurationError` for configuration issues
- Example scripts
  - `basic_usage.py` - Basic dual camera operations
  - `advanced_usage.py` - Advanced features including video recording
  - `single_camera.py` - Single camera usage
- Comprehensive documentation
  - Installation guide
  - Quick start examples
  - API reference
  - Troubleshooting guide
- Package setup files
  - `requirements.txt` with opencv-python dependency
  - `setup.py` for package installation
  - `.gitignore` for Python projects
  - MIT License

### Technical Details
- Built on OpenCV (cv2) for camera interface
- Supports Python 3.7+
- Proper attribute initialization to prevent AttributeError
- Cached cv2 import for performance
- Comprehensive logging using Python's logging module
- Type hints for better IDE support
