"""
Basic example of using Kaderblick Dual Camera Control.

This example demonstrates:
- Opening cameras
- Capturing images from both cameras
- Closing cameras properly
"""

import sys
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
    """Main function demonstrating basic camera usage."""
    
    logger.info("Starting Kaderblick Dual Camera basic example")
    
    try:
        # Create dual camera instance with default settings
        # Camera 1 on device 0, Camera 2 on device 1
        dual_camera = DualCamera(camera1_id=0, camera2_id=1)
        
        logger.info("Opening cameras...")
        dual_camera.open()
        
        logger.info("Cameras opened successfully")
        logger.info(f"Camera 1: {dual_camera.camera1}")
        logger.info(f"Camera 2: {dual_camera.camera2}")
        
        # Capture images from both cameras
        logger.info("Capturing images from both cameras...")
        image1_path, image2_path = dual_camera.capture_images()
        
        logger.info(f"Images captured successfully:")
        logger.info(f"  Camera 1: {image1_path}")
        logger.info(f"  Camera 2: {image2_path}")
        
        # Close cameras
        logger.info("Closing cameras...")
        dual_camera.close()
        
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
