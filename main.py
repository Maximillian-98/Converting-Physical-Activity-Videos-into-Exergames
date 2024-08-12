import cv2
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from PIL import Image, ImageTk
import numpy as np
import json

class videoPose:
    def __init__(self, video_path, output_path, angles_output_path):
        self.video_path = video_path
        self.output_path = output_path
        self.angles_output_path = angles_output_path
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

        self.visibility_threshold = 0.8

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

            # Calculate angles and save them
            angles = self.calculateAllAngles()
            
            # Play the video
            cv2.imshow('Mediapipe Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            # Write the frame to the output video
            self.out.write(image) 

            # Write angles to json file
            self.saveAngles(angles)

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

    # Save angles to file
    def saveAngles(self, angles_dict):
        with open(self.angles_output_path, 'w') as f:
            json.dump(angles_dict, f, indent = 4)


    # Visibilty check for keypoints
    def visibleCheck(self, keypoints):
        for idx in keypoints:
            if self.landmarks[idx].visibility > self.visibility_threshold:
                return True
        return False

    # Angle points
    def calculateAngle(self, keypoints):
        
        # For tomorrow, if this doesnt work, try pluggin in a bunch of print statements again to see the problems
        a = self.landmarks[keypoints[0]]
        b = self.landmarks[keypoints[1]]
        c = self.landmarks[keypoints[2]]

        if self.visibleCheck(keypoints):
            radians = np.arctan2(c.y-b.y, c.x-b.x) - np.arctan2(a.y-b.y, a.x-b.x)
            angle = np.abs(radians*180.0/np.pi)
        
            if angle >180.0:
                angle = 360-angle

            return angle
        else:
            return None
    
    def calculateAllAngles(self):
        angles = {}
        left_arm = [11, 13, 15]
        right_arm = [12, 14, 16]
        left_leg = [23, 25, 27]
        right_leg = [24, 26, 28]
        left_hip = [11, 23, 25]
        right_hip = [12, 24, 26]

        angles["left_arm"] = self.calculateAngle(left_arm)
        angles["right_arm"] = self.calculateAngle(right_arm)
        angles["left_leg"] = self.calculateAngle(left_leg)
        angles["right_leg"] = self.calculateAngle(right_leg)
        angles["left_hip"] = self.calculateAngle(left_hip)
        angles["right_hip"] = self.calculateAngle(right_hip)

        return angles



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

        self.visibility_threshold = 0.8

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
                point1 = self.landmarks[idx1]
                point2 = self.landmarks[idx2]
                if point1.visibility > self.visibility_threshold and point2.visibility > self.visibility_threshold:
                    cv2.line(image, 
                            (int(point1.x * image.shape[1]), int(point1.y * image.shape[0])),
                            (int(point2.x * image.shape[1]), int(point2.y * image.shape[0])),
                            (0, 0, 245), 2)

            # Draw keypoints
            for idx in self.keypoint_indices:
                if self.landmarks[idx].visibility > self.visibility_threshold:
                    point = self.landmarks[idx]
                    cv2.circle(image,
                            (int(point.x * image.shape[1]), int(point.y * image.shape[0])),
                            5, (245, 0, 0), -1)
            
            # Calculate the angle of the body parts, return each angle
            angles = self.calculateAllAngles()
            # Successfully print angles
            # print(angles)

            return image

        self.cap.release()
        cv2.destroyAllWindows()

    # Visibilty check for keypoints
    def visibleCheck(self, keypoints):
        for idx in keypoints:
            if self.landmarks[idx].visibility > self.visibility_threshold:
                return True
        return False

    # Angle points
    def calculateAngle(self, keypoints):
        
        # For tomorrow, if this doesnt work, try pluggin in a bunch of print statements again to see the problems
        a = self.landmarks[keypoints[0]]
        b = self.landmarks[keypoints[1]]
        c = self.landmarks[keypoints[2]]

        if self.visibleCheck(keypoints):
            radians = np.arctan2(c.y-b.y, c.x-b.x) - np.arctan2(a.y-b.y, a.x-b.x)
            angle = np.abs(radians*180.0/np.pi)
        
            if angle >180.0:
                angle = 360-angle

            return angle
        else:
            return None
    
    def calculateAllAngles(self):
        angles = {}
        left_arm = [11, 13, 15]
        right_arm = [12, 14, 16]
        left_leg = [23, 25, 27]
        right_leg = [24, 26, 28]
        left_hip = [11, 23, 25]
        right_hip = [12, 24, 26]

        angles["left_arm"] = self.calculateAngle(left_arm)
        angles["right_arm"] = self.calculateAngle(right_arm)
        angles["left_leg"] = self.calculateAngle(left_leg)
        angles["right_leg"] = self.calculateAngle(right_leg)
        angles["left_hip"] = self.calculateAngle(left_hip)
        angles["right_hip"] = self.calculateAngle(right_hip)

        return angles


    # Distance points


    # Normalisation
        

# self.landmark contains an object of objects,
# self.landmark[idx] contains an object of the x y z coordinates of the body part defined by idx (11 is right shoulders)


#video_path = r'C:\Users\max\Documents\GitHub\Converting-Physical-Activity-Videos-into-Exergames\Exercise Videos\PushupsTop.mp4'

#video_landmarker = videoPose(video_path)
#video_landmarker.drawPose

#live_landmarker = livePose()
#live_landmarker.drawPose()

# This was at the end of livePose

# Place in Draw keypoints: print(self.landmarks[idx].visibility)

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