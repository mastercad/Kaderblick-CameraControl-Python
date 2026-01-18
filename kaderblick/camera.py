"""
Core camera control implementation for Kaderblick cameras.
"""

import logging
import time
from typing import Optional, Tuple, List, Any
from datetime import datetime
from pathlib import Path

from .config import CameraConfig
from .exceptions import (
    CameraConnectionError,
    CameraOperationError,
)

logger = logging.getLogger(__name__)


class Camera:
    """Class representing a single Kaderblick camera."""

    def __init__(
        self,
        device_id: int = 0,
        config: Optional[CameraConfig] = None,
        name: str = "Camera"
    ):
        """
        Initialize a camera instance.

        Args:
            device_id: Camera device ID (0, 1, 2, etc.)
            config: Optional CameraConfig instance
            name: Name identifier for the camera
        """
        self.device_id = device_id
        self.name = name
        self.config = config or CameraConfig()
        self._is_open = False
        self._capture = None
        self._recording = False
        self._video_writer = None
        self._recording_filepath = None
        self._cv2 = None
        
        logger.info(f"Initializing {self.name} with device ID {device_id}")

    def open(self) -> None:
        """
        Open camera device connection.

        Raises:
            CameraConnectionError: If connection fails
        """
        try:
            # Import cv2 only when needed and cache it
            if self._cv2 is None:
                import cv2
                self._cv2 = cv2
            
            self._capture = self._cv2.VideoCapture(self.device_id)
            
            if not self._capture.isOpened():
                raise CameraConnectionError(
                    f"Failed to open camera {self.name} (device {self.device_id})"
                )
            
            # Apply configuration
            self._apply_config()
            self._is_open = True
            logger.info(f"{self.name} opened successfully")
            
        except ImportError:
            raise CameraConnectionError(
                "OpenCV (cv2) is not installed. Install with: pip install opencv-python"
            )
        except Exception as e:
            raise CameraConnectionError(f"Failed to open camera: {e}")

    def _apply_config(self) -> None:
        """Apply configuration settings to camera."""
        if not self._capture or not self._cv2:
            return
        
        resolution = self.config.get("resolution")
        if resolution:
            self._capture.set(self._cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
            self._capture.set(self._cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        
        fps = self.config.get("fps")
        if fps:
            self._capture.set(self._cv2.CAP_PROP_FPS, fps)
        
        brightness = self.config.get("brightness")
        if brightness is not None:
            self._capture.set(self._cv2.CAP_PROP_BRIGHTNESS, brightness / 100.0)
        
        contrast = self.config.get("contrast")
        if contrast is not None:
            self._capture.set(self._cv2.CAP_PROP_CONTRAST, contrast / 100.0)
        
        saturation = self.config.get("saturation")
        if saturation is not None:
            self._capture.set(self._cv2.CAP_PROP_SATURATION, saturation / 100.0)

    def close(self) -> None:
        """Close camera device connection."""
        if self._capture:
            self._capture.release()
            self._capture = None
            self._is_open = False
            logger.info(f"{self.name} closed")

    def is_open(self) -> bool:
        """Check if camera is open."""
        return self._is_open

    def capture_image(self, filepath: Optional[str] = None) -> Optional[str]:
        """
        Capture a single image from camera.

        Args:
            filepath: Optional path to save image. If None, auto-generates filename.

        Returns:
            Path to saved image file, or None if capture failed

        Raises:
            CameraOperationError: If capture fails
        """
        if not self._is_open or not self._cv2:
            raise CameraOperationError(f"{self.name} is not open")
        
        ret, frame = self._capture.read()
        
        if not ret:
            raise CameraOperationError(f"Failed to capture image from {self.name}")
        
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"{self.name}_{timestamp}.jpg"
        
        self._cv2.imwrite(filepath, frame)
        logger.info(f"{self.name} captured image: {filepath}")
        
        return filepath

    def start_recording(self, filepath: Optional[str] = None, codec: str = 'MJPG') -> str:
        """
        Start recording video.

        Args:
            filepath: Optional path to save video. If None, auto-generates filename.
            codec: Video codec (default: MJPG)

        Returns:
            Path to video file

        Raises:
            CameraOperationError: If recording fails to start
        """
        if not self._is_open or not self._cv2:
            raise CameraOperationError(f"{self.name} is not open")
        
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"{self.name}_{timestamp}.avi"
        
        fps = self.config.get("fps", 30)
        resolution = self.config.get("resolution", (1920, 1080))
        
        fourcc = self._cv2.VideoWriter_fourcc(*codec)
        self._video_writer = self._cv2.VideoWriter(filepath, fourcc, fps, resolution)
        
        if not self._video_writer.isOpened():
            raise CameraOperationError(f"Failed to start recording on {self.name}")
        
        self._recording = True
        self._recording_filepath = filepath
        logger.info(f"{self.name} started recording: {filepath}")
        
        return filepath

    def write_frame(self) -> None:
        """Write a frame during recording."""
        if not self._recording:
            return
        
        ret, frame = self._capture.read()
        if ret:
            self._video_writer.write(frame)

    def stop_recording(self) -> Optional[str]:
        """
        Stop recording video.

        Returns:
            Path to recorded video file, or None if not recording
        """
        if not self._recording:
            logger.warning(f"{self.name} is not recording")
            return None
        
        if self._video_writer:
            self._video_writer.release()
        self._recording = False
        filepath = self._recording_filepath
        self._recording_filepath = None
        logger.info(f"{self.name} stopped recording: {filepath}")
        
        return filepath

    def get_frame(self):
        """
        Get current frame from camera.

        Returns:
            Tuple of (success, frame) where success is bool and frame is numpy array

        Raises:
            CameraOperationError: If camera is not open
        """
        if not self._is_open or not self._cv2:
            raise CameraOperationError(f"{self.name} is not open")
        
        return self._capture.read()

    def set_property(self, property_name: str, value: Any) -> None:
        """
        Set camera property.

        Args:
            property_name: Name of property in config
            value: Value to set
        """
        self.config.set(property_name, value)
        if self._is_open:
            self._apply_config()

    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __repr__(self) -> str:
        status = "open" if self._is_open else "closed"
        return f"Camera(name='{self.name}', device_id={self.device_id}, status={status})"


class DualCamera:
    """Class for controlling two Kaderblick cameras simultaneously."""

    def __init__(
        self,
        camera1_id: int = 0,
        camera2_id: int = 1,
        config1: Optional[CameraConfig] = None,
        config2: Optional[CameraConfig] = None,
    ):
        """
        Initialize dual camera system.

        Args:
            camera1_id: Device ID for first camera
            camera2_id: Device ID for second camera
            config1: Optional configuration for first camera
            config2: Optional configuration for second camera
        """
        self.camera1 = Camera(camera1_id, config1, name="Camera1")
        self.camera2 = Camera(camera2_id, config2, name="Camera2")
        logger.info("Initialized dual camera system")

    def open(self) -> None:
        """Open both cameras."""
        self.camera1.open()
        self.camera2.open()
        logger.info("Both cameras opened")

    def close(self) -> None:
        """Close both cameras."""
        self.camera1.close()
        self.camera2.close()
        logger.info("Both cameras closed")

    def capture_images(
        self,
        filepath1: Optional[str] = None,
        filepath2: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Capture images from both cameras simultaneously.

        Args:
            filepath1: Optional path for first camera image
            filepath2: Optional path for second camera image

        Returns:
            Tuple of (filepath1, filepath2) with paths to saved images
        """
        path1 = self.camera1.capture_image(filepath1)
        path2 = self.camera2.capture_image(filepath2)
        logger.info(f"Captured images from both cameras: {path1}, {path2}")
        return path1, path2

    def start_recording(
        self,
        filepath1: Optional[str] = None,
        filepath2: Optional[str] = None,
        codec: str = 'MJPG'
    ) -> Tuple[str, str]:
        """
        Start recording from both cameras.

        Args:
            filepath1: Optional path for first camera video
            filepath2: Optional path for second camera video
            codec: Video codec (default: MJPG)

        Returns:
            Tuple of (filepath1, filepath2) with paths to video files
        """
        path1 = self.camera1.start_recording(filepath1, codec)
        path2 = self.camera2.start_recording(filepath2, codec)
        logger.info(f"Started recording from both cameras: {path1}, {path2}")
        return path1, path2

    def write_frames(self) -> None:
        """Write frames from both cameras during recording."""
        self.camera1.write_frame()
        self.camera2.write_frame()

    def stop_recording(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Stop recording from both cameras.

        Returns:
            Tuple of (filepath1, filepath2) with paths to recorded files
        """
        path1 = self.camera1.stop_recording()
        path2 = self.camera2.stop_recording()
        logger.info(f"Stopped recording from both cameras")
        return path1, path2

    def get_frames(self):
        """
        Get current frames from both cameras.

        Returns:
            Tuple of ((success1, frame1), (success2, frame2))
        """
        frame1 = self.camera1.get_frame()
        frame2 = self.camera2.get_frame()
        return frame1, frame2

    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __repr__(self) -> str:
        return f"DualCamera(camera1={self.camera1}, camera2={self.camera2})"
