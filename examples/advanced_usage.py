"""
Advanced example of using Kaderblick Dual Camera Control.

This example demonstrates:
- Using custom configurations
- Recording video from both cameras
- Using context managers for automatic cleanup
- Adjusting camera settings
"""

import sys
import time
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from kaderblick import DualCamera, CameraConfig
from kaderblick.exceptions import CameraConnectionError, CameraOperationError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating advanced camera usage."""
    
    logger.info("Starting Kaderblick Dual Camera advanced example")
    
    try:
        # Create custom configurations for each camera
        config1 = CameraConfig({
            "resolution": (1280, 720),
            "fps": 30,
            "brightness": 60,
            "contrast": 55,
        })
        
        config2 = CameraConfig({
            "resolution": (1280, 720),
            "fps": 30,
            "brightness": 50,
            "contrast": 50,
        })
        
        # Use context manager for automatic cleanup
        logger.info("Opening cameras with custom configurations...")
        with DualCamera(camera1_id=0, camera2_id=1, config1=config1, config2=config2) as dual_camera:
            
            logger.info("Cameras opened successfully")
            
            # Capture initial images
            logger.info("Capturing initial images...")
            dual_camera.capture_images("camera1_initial.jpg", "camera2_initial.jpg")
            
            # Adjust camera settings dynamically
            logger.info("Adjusting camera 1 brightness...")
            dual_camera.camera1.set_property("brightness", 70)
            
            # Capture another image with new settings
            logger.info("Capturing image with adjusted settings...")
            dual_camera.camera1.capture_image("camera1_adjusted.jpg")
            
            # Start recording from both cameras
            logger.info("Starting video recording from both cameras...")
            video1_path, video2_path = dual_camera.start_recording(
                "camera1_recording.avi",
                "camera2_recording.avi"
            )
            
            # Record for 5 seconds
            logger.info("Recording for 5 seconds...")
            start_time = time.time()
            while time.time() - start_time < 5:
                dual_camera.write_frames()
                time.sleep(0.033)  # ~30 FPS
            
            # Stop recording
            logger.info("Stopping recording...")
            dual_camera.stop_recording()
            
            logger.info(f"Recordings saved:")
            logger.info(f"  Camera 1: {video1_path}")
            logger.info(f"  Camera 2: {video2_path}")
        
        # Cameras are automatically closed when exiting context manager
        logger.info("Example completed successfully!")
        
    except CameraConnectionError as e:
        logger.error(f"Camera connection error: {e}")
        logger.error("Make sure cameras are connected and device IDs are correct")
        sys.exit(1)
        
    except CameraOperationError as e:
        logger.error(f"Camera operation error: {e}")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
