import cv2
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from PIL import Image, ImageTk
import numpy as np

class videoPose:
    def __init__(self, video_path, output_path):
        self.video_path = video_path
        self.output_path = output_path
        self.cap = cv2.VideoCapture(self.video_path)

        # Get video properties
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Initialize VideoWriter
        self.out = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))

        # Setup drawing tools
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        # Setup mediapipe instance
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def drawPose(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = self.pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Render detections
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                    self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            # Write the frame to the output video file
            self.out.write(image)
            
            # Display the frame
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

class livePose:
    def __init__(self, canvas):
        self.cap = cv2.VideoCapture(0)

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        # Setup mediapipe instance
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Canvas input so the feed appears within the selected canvas
        self.canvas = self.canvas

    def drawPose(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = self.pose.process(image)

            '''
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            '''

            # Render detections
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                    self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )           

            # Convert image to PhotoImage
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            
            # Update canvas with the image
            self.canvas.create_image(0, 0, image=photo, anchor='nw')
            self.canvas.update_idletasks()
            self.canvas.update()    
            
            '''
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            '''

        self.cap.release()
        cv2.destroyAllWindows()

video_path = r'C:\Users\max\Documents\GitHub\Converting-Physical-Activity-Videos-into-Exergames\Exercise Videos\PushupsTop.mp4'

#video_landmarker = videoPose(video_path)
#video_landmarker.drawPose

#live_landmarker = livePose()
#live_landmarker.drawPose()