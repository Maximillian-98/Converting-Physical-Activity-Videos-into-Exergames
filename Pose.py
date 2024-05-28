import cv2
import mediapipe as mp

class PoselandmarkdetectionVIDEO:
    def __init__(self):
        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the video mode:
        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO)
        
        self.landmarker = PoseLandmarker.create_from_options(options)

# The __enter__ method returns the landmarker instance, allowing the class to be used with a with statement.
    def __enter__(self):
        return self.landmarker
# The __exit__ method ensures the landmarker is properly closed when exiting the with block.
    def __exit__(self, exc_type, exc_value, traceback):
        self.landmarker.close()


