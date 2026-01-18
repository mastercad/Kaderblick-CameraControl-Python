"""
Single camera example of using Kaderblick Camera Control.

This example demonstrates:
- Using a single camera instead of dual cameras
- Basic camera operations
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from kaderblick import Camera, CameraConfig
from kaderblick.exceptions import CameraConnectionError, CameraOperationError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating single camera usage."""
    
    logger.info("Starting Kaderblick single camera example")
    
    try:
        # Create custom configuration
        config = CameraConfig({
            "resolution": (1920, 1080),
            "fps": 30,
            "brightness": 55,
        })
        
        # Use context manager for automatic cleanup
        logger.info("Opening camera...")
        with Camera(device_id=0, config=config, name="MainCamera") as camera:
            
            logger.info(f"Camera opened: {camera}")
            
            # Capture an image
            logger.info("Capturing image...")
            image_path = camera.capture_image("single_camera_image.jpg")
            logger.info(f"Image saved: {image_path}")
        
        logger.info("Example completed successfully!")
        
    except CameraConnectionError as e:
        logger.error(f"Camera connection error: {e}")
        logger.error("Make sure camera is connected and device ID is correct")
        sys.exit(1)
        
    except CameraOperationError as e:
        logger.error(f"Camera operation error: {e}")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
