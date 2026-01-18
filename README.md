# Kaderblick-CameraControl-Python

Python interface for controlling Kaderblick dual camera systems via Python device.

## Features

- **Dual Camera Support**: Control two cameras simultaneously
- **Single Camera Mode**: Use individual cameras independently
- **Image Capture**: Capture still images from one or both cameras
- **Video Recording**: Record video streams from cameras
- **Configurable Settings**: Adjust resolution, FPS, brightness, contrast, and more
- **Easy to Use**: Simple API with context manager support
- **Error Handling**: Comprehensive exception handling for robust operation

## Installation

### From Source

```bash
git clone https://github.com/mastercad/Kaderblick-CameraControl-Python.git
cd Kaderblick-CameraControl-Python
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

### Requirements

- Python 3.7+
- OpenCV (opencv-python)
- NumPy

## Quick Start

### Basic Dual Camera Usage

```python
from kaderblick import DualCamera

# Create dual camera instance
dual_camera = DualCamera(camera1_id=0, camera2_id=1)

# Open cameras
dual_camera.open()

# Capture images from both cameras
image1_path, image2_path = dual_camera.capture_images()
print(f"Images saved: {image1_path}, {image2_path}")

# Close cameras
dual_camera.close()
```

### Using Context Manager

```python
from kaderblick import DualCamera

# Automatically handles opening and closing
with DualCamera(camera1_id=0, camera2_id=1) as dual_camera:
    # Capture images
    dual_camera.capture_images("cam1.jpg", "cam2.jpg")
```

### Single Camera Usage

```python
from kaderblick import Camera, CameraConfig

# Create custom configuration
config = CameraConfig({
    "resolution": (1920, 1080),
    "fps": 30,
    "brightness": 60
})

# Use single camera
with Camera(device_id=0, config=config, name="MainCamera") as camera:
    camera.capture_image("photo.jpg")
```

### Video Recording

```python
import time
from kaderblick import DualCamera

with DualCamera() as dual_camera:
    # Start recording
    video1, video2 = dual_camera.start_recording()
    
    # Record for 5 seconds
    start = time.time()
    while time.time() - start < 5:
        dual_camera.write_frames()
        time.sleep(0.033)  # ~30 FPS
    
    # Stop recording
    dual_camera.stop_recording()
    print(f"Videos saved: {video1}, {video2}")
```

## Configuration

The `CameraConfig` class allows you to customize camera settings:

```python
from kaderblick import CameraConfig

config = CameraConfig({
    "resolution": (1920, 1080),  # Width x Height
    "fps": 30,                    # Frames per second
    "brightness": 50,             # 0-100
    "contrast": 50,               # 0-100
    "saturation": 50,             # 0-100
    "auto_exposure": True,
    "auto_white_balance": True,
})

# Save configuration to file
config.save("camera_config.json")

# Load configuration from file
config = CameraConfig.load("camera_config.json")
```

## Examples

The `examples/` directory contains several example scripts:

- `basic_usage.py`: Basic dual camera operation
- `advanced_usage.py`: Advanced features including video recording
- `single_camera.py`: Single camera usage

Run an example:

```bash
python examples/basic_usage.py
```

## API Reference

### DualCamera

Main class for controlling two cameras simultaneously.

**Methods:**
- `open()`: Open both cameras
- `close()`: Close both cameras
- `capture_images(filepath1, filepath2)`: Capture images from both cameras
- `start_recording(filepath1, filepath2, codec)`: Start recording video
- `write_frames()`: Write frames during recording
- `stop_recording()`: Stop recording
- `get_frames()`: Get current frames from both cameras

### Camera

Class for controlling a single camera.

**Methods:**
- `open()`: Open camera connection
- `close()`: Close camera connection
- `is_open()`: Check if camera is open
- `capture_image(filepath)`: Capture single image
- `start_recording(filepath, codec)`: Start video recording
- `write_frame()`: Write a frame during recording
- `stop_recording()`: Stop recording
- `get_frame()`: Get current frame
- `set_property(name, value)`: Set camera property

### CameraConfig

Configuration management class.

**Methods:**
- `get(key, default)`: Get configuration value
- `set(key, value)`: Set configuration value
- `update(config_dict)`: Update multiple values
- `save(filepath)`: Save to JSON file
- `load(filepath)`: Load from JSON file (class method)

## Error Handling

The package provides specific exceptions for different error cases:

```python
from kaderblick import Camera
from kaderblick.exceptions import (
    CameraConnectionError,
    CameraOperationError,
    ConfigurationError
)

try:
    camera = Camera(device_id=0)
    camera.open()
    camera.capture_image()
except CameraConnectionError as e:
    print(f"Failed to connect to camera: {e}")
except CameraOperationError as e:
    print(f"Camera operation failed: {e}")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
finally:
    camera.close()
```

## Troubleshooting

### Camera Not Found

If you get a `CameraConnectionError`, check:
1. Camera is properly connected
2. Camera drivers are installed
3. Correct device ID is being used (try 0, 1, 2, etc.)
4. No other application is using the camera

### OpenCV Not Installed

If you get an import error for cv2:
```bash
pip install opencv-python
```

### Permission Issues (Linux)

On Linux, you may need to add your user to the video group:
```bash
sudo usermod -a -G video $USER
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.