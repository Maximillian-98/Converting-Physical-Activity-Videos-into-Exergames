import cv2
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import os

# For drawing on to the image
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

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


# Custom Landmarks, Can be edited to change the which landmarks are drawn etc...
    def draw_landmarks_on_image(self, rgb_image, detection_result):
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(rgb_image)

        # Loop through the detected poses to visualize.
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
        return annotated_image

    
# Processes the video and creates and maps the landmarks
    def process_video(self):
        frame_index = 0
        success, frame = self.cap.read()
        while success:
            # Convert the frame received from OpenCV to a MediaPipe’s Image object.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            # Get image timestamp from frame
            frame_timestamp = int((frame_index / self.fps) * 1000)

            # Detect pose landmarks from image and stores them
            pose_landmarks = self.landmarker.detect_for_video(mp_image, frame_timestamp)
            
            # STEP 5: Process the detection result. In this case, visualize it.
            annotated_image = self.draw_landmarks_on_image(mp_image.numpy_view(), pose_landmarks)
            cv2.imshow('Video_Feed',cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

            # Apply visual landmarks to video
            # Currently this uses a premade utility from the mp library
            #pose_image = mp_drawing.draw_landmarks(mp_image, pose_landmarks.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # Shows the video running
            #cv2.imshow('Video_feed', annotated_image)
            
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
# model_path = r'C:\Users\max\Documents\GitHub\Converting-Physical-Activity-Videos-into-Exergames\Landmarkers\pose_landmarker_full.task'
model_path = 'pose_landmarker_full.task'
video_path = r'C:\Users\max\Documents\GitHub\Converting-Physical-Activity-Videos-into-Exergames\Exercise Videos\PushupsTop.mp4'

video_landmarker = PoselandmarkdetectionVIDEO(model_path, video_path)
video_landmarker.process_video()

# Need to finish, add poselanmarkerresult to get the returned object 