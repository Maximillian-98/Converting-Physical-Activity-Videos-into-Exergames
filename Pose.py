import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

class PoselandmarkdetectionVIDEO:
    def __init__(self, model_path, video_path):
        self.model_path = model_path
        self.video_path = video_path

        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the video mode:
        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO)
        
        self.landmarker = PoseLandmarker.create_from_options(options)

# Initialise video capture
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened(): #Checks if it opens properly
            raise ValueError("Error opening video file")
        
# Video Properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) #Used for timestamping each frame

    
# Processes the video and creates and maps the landmarks
    def process_video(self):
        frame_index = 0
        success, frame = self.cap.read()
        while success:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            timestamp_ms = (frame_index / self.fps) * 1000
            pose_landmarks = self.landmarker.detect_for_video(mp_image, timestamp_ms)
            
            # Add here the landmarker stuff to output the object
            
            # Read the next frame
            success, frame = self.cap.read()
            frame_index += 1

# The __enter__ method returns the landmarker instance, allowing the class to be used with a with statement.
    def __enter__(self):
        return self.landmarker
# The __exit__ method ensures the landmarker is properly closed when exiting the with block.
    def __exit__(self, exc_type, exc_value, traceback):
        self.landmarker.close()
        self.cap.release()


# Need to finish, add poselanmarkerresult to get the returned object 