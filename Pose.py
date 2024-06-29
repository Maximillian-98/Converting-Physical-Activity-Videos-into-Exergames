import cv2
import mediapipe as mp
import numpy as np
import os

# For drawing on to the image
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Make the pose method to use to process the image later
pose = mp_pose.Pose()

class PoselandmarkdetectionVIDEO:
    def __init__(self, model_path, video_path):
        self.model_path = model_path
        self.video_path = video_path

        # Having trouble with landmarker so adding this path check
        if not os.path.exists(self.model_path):
            raise ValueError(f"Model file not found: {self.model_path}")

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
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened(): #Checks if it opens properly
            raise ValueError("Error opening video file")
        
# Video Properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) #Used for timestamping each frame

    
# Processes the video and creates and maps the landmarks
    def process_video(self):
        frame_index = 0
        success, frame = self.cap.read()
        while success:
            # Recolor image to RGB, openCV is in BGR
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get image timestamp from frame
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            timestamp = int((frame_index / self.fps) * 1000)

            # Detect pose landmarks from image
            pose_landmarks = self.landmarker.detect_for_video(mp_image, timestamp)

            print(pose_landmarks.pose_landmarks)

            # Apply visual landmarks to video
            # Currently this uses a premade utility from the mp library
            # mp_drawing.draw_landmarks(mp_image, pose_landmarks.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # Shows the video running
            cv2.imshow('Video_feed', mp_image)
            
            # Read the next frame
            success, frame = self.cap.read()
            frame_index += 1

            # Break the loop if ESC key is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

# The __enter__ method returns the landmarker instance, allowing the class to be used with a with statement.
    def __enter__(self):
        return self
# The __exit__ method ensures the landmarker is properly closed when exiting the with block.
    def __exit__(self, exc_type, exc_value, traceback):
        self.landmarker.close()
        self.cap.release()

# These need to be moved so that they are options in the UI
model_path = r'C:\Users\max\Documents\Bath Uni Dissertation\Landmarkers\pose_landmarker_lite.task'
video_path = 'C:\\Users\\max\\Documents\\Bath Uni Dissertation\\Exercise Videos\\PushupsTop.mp4'

video_landmarker = PoselandmarkdetectionVIDEO(model_path, video_path)
video_landmarker.process_video()

# Need to finish, add poselanmarkerresult to get the returned object 