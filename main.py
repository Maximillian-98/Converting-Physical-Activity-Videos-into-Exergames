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

        # Keypoints for drawing
        self.keypoint_indices = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
        self.connections = [(11, 13), (13, 15), # Left arm
                            (12, 14), (14, 16), # Right arm
                            (11, 12), (11, 23), (12, 24), (23, 24), # Torso
                            (23, 25), (25, 27), # Left leg
                            (24, 26), (26, 28), # Left leg
                            ]
        
        # Initialise landmarks attribute
        self.landmarks = {}

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

            # Extract Landmarks
            try:
                self.landmarks = results.pose_landmarks.landmark
                #print(landmarks)
            except:
                pass
            
            # Render detections
            # Draw keypoints and selected connections
            for i, (idx1, idx2) in enumerate(self.connections):
                point1 = results.pose_landmarks.landmark[idx1]
                point2 = results.pose_landmarks.landmark[idx2]
                cv2.line(image, 
                        (int(point1.x * image.shape[1]), int(point1.y * image.shape[0])),
                        (int(point2.x * image.shape[1]), int(point2.y * image.shape[0])),
                        (0, 0, 245), 2)

            for idx in self.keypoint_indices:
                point = results.pose_landmarks.landmark[idx]
                cv2.circle(image,
                        (int(point.x * image.shape[1]), int(point.y * image.shape[0])),
                        5, (245, 0, 0), -1)      

            # This causes the thumbnails to break
            # image = cv2.resize(image, (1000, 800))
            
            # Play the video
            cv2.imshow('Mediapipe Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            # Write the frame to the output video
            self.out.write(image) 

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()



class livePose:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        # Keypoints for drawing
        self.keypoint_indices = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
        self.connections = [(11, 13), (13, 15), # Left arm
                            (12, 14), (14, 16), # Right arm
                            (11, 12), (11, 23), (12, 24), (23, 24), # Torso
                            (23, 25), (25, 27), # Left leg
                            (24, 26), (26, 28), # Right leg
                            ]
        
        # Initialise landmarks attribute
        self.landmarks = {}

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

            # Extract Landmarks
            try:
                self.landmarks = results.pose_landmarks.landmark
            except:
                pass

            # Render detections
            # Draw selected connections
            for i, (idx1, idx2) in enumerate(self.connections):
                point1 = results.pose_landmarks.landmark[idx1]
                point2 = results.pose_landmarks.landmark[idx2]
                cv2.line(image, 
                        (int(point1.x * image.shape[1]), int(point1.y * image.shape[0])),
                        (int(point2.x * image.shape[1]), int(point2.y * image.shape[0])),
                        (0, 0, 245), 2)

            # Draw keypoints
            for idx in self.keypoint_indices:
                point = results.pose_landmarks.landmark[idx]
                cv2.circle(image,
                        (int(point.x * image.shape[1]), int(point.y * image.shape[0])),
                        5, (245, 0, 0), -1)
            

            return image

        self.cap.release()
        cv2.destroyAllWindows()

    # Visibilty check for keypoints
    def visibleCheck(self, keypoints):
        visibility_threshold = 0.5
        for idx in keypoints:
            if self.landmarks[idx]["visibility"] < visibility_threshold:
                return False
        return True

    # Angle points
    def calculateAngle(self, a, b, c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
    
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
    
        if angle >180.0:
            angle = 360-angle
        
        return angle
    
    def calculateAllAngles(self, landmarks):
        angles = {}
        left_arm = [11, 13, 15]

        if self.visibleCheck(left_arm, landmarks):
            angles["left_arm"] = self.calculateAngle(landmarks[left_arm[0]], landmarks[left_arm[1]], landmarks[left_arm[2]])
        else:
            return None

    # Distance points


    # Normalisation
        

#video_path = r'C:\Users\max\Documents\GitHub\Converting-Physical-Activity-Videos-into-Exergames\Exercise Videos\PushupsTop.mp4'

#video_landmarker = videoPose(video_path)
#video_landmarker.drawPose

#live_landmarker = livePose()
#live_landmarker.drawPose()

# This was at the end of livePose
'''
            # Update canvas with the image
            self.canvas.create_image(0, 0, image=photo, anchor='nw')
            self.canvas.update_idletasks()
            self.canvas.update()    
            
            
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        '''

'''
            # Old drawing method
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                    self.mp_drawing.DrawingSpec(color=(245,0,0), thickness=2, circle_radius=2),
                                    self.mp_drawing.DrawingSpec(color=(0,0,245), thickness=2, circle_radius=2) 
                                    )   
            '''   