import cv2
from PIL import Image
import numpy as np

def video_to_pillow_frames(video_path):
    """
    Extract frames from a video and convert them to Pillow Images.
    
    Parameters:
        video_path (str): Path to the video file
        
    Returns:
        generator: Yields Pillow Image objects for each frame
    """
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        raise ValueError("Could not open video file")
    
    try:
        while True:
            # Read the next frame
            success, frame = video.read()
            
            if not success:
                break
                
            # OpenCV uses BGR format, convert to RGB for Pillow
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to Pillow Image
            pil_image = Image.fromarray(rgb_frame)
            
            yield pil_image
            
    finally:
        # Always release the video capture object
        video.release()

def get_video_info(video_path):
    """
    Get basic information about the video.
    
    Returns:
        dict: Video information including fps, frame count, and dimensions
    """
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        raise ValueError("Could not open video file")
    
    try:
        # Get video properties
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        return {
            'fps': fps,
            'frame_count': frame_count,
            'width': width,
            'height': height,
            'duration': frame_count / fps if fps else 0
        }
    
    finally:
        video.release()

# Example usage
if __name__ == "__main__":
    video_path = "path_to_your_video.mp4"
    
    try:
        # Print video information
        info = get_video_info(video_path)
        print(f"Video Info:")
        print(f"FPS: {info['fps']}")
        print(f"Frame Count: {info['frame_count']}")
        print(f"Dimensions: {info['width']}x{info['height']}")
        print(f"Duration: {info['duration']:.2f} seconds")
        
        # Process frames
        for i, frame in enumerate(video_to_pillow_frames(video_path)):

            print(f"Processing frame {frame}")
            # Do something with each frame
            # For example, save it:
            # frame.save(f"frame_{i:04d}.jpg")
            
            # Or process it:
            # processed_frame = your_processing_function(frame)
            pass
            
    except Exception as e:
        print(f"Error: {e}")