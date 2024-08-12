import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk # For getting image for thumbnail
from main import videoPose, livePose
import os
import numpy as np
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import json

class MainFrame:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout App")

        self.windowPlacey = 0.1
        self.windowHeight = 0.65
        self.buttonPlacey = 0.75

        self.selected_thumbnail = None

        # Create Base canvas layer
        self.canvas = tk.Canvas(self.root, width=1000, height=800, bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        # Text
        self.title = tk.Label(self.canvas, text="To be Named")
        self.title.place(relx=0.45, rely=0, relwidth=0.1, relheight=0.05)
        self.exVidTitle = tk.Label(self.canvas, text="Exercise Videos")
        self.exVidTitle.place(relx=0.2, rely=0.05, relwidth=0.1, relheight=0.05)
        self.workoutTitle = tk.Label(self.canvas, text="Workout")
        self.workoutTitle.place(relx=0.7, rely=0.05, relwidth=0.1, relheight=0.05)
        self.breakText = tk.Label(self.canvas, text="Current Break length:")
        self.breakText.place(relx=0.1, rely=0.9, relwidth=0.15, relheight=0.05)
        self.breakTime = tk.Label(self.canvas, text="00:00")
        self.breakTime.place(relx=0.25, rely=0.9, relwidth=0.1, relheight=0.05)

        self.breakEntry = tk.Entry(self.canvas)
        self.breakEntry.place(relx=0.1, rely=0.85, relwidth=0.15, relheight=0.05)

        # Buttons
        self.uploadButton = tk.Button(self.canvas, text="Upload", command=self.upload)
        self.uploadButton.place(relx=0.1, rely=self.buttonPlacey, relwidth=0.1, relheight=0.05)
        self.deleteButton = tk.Button(self.canvas, text="Delete", command=self.delete)
        self.deleteButton.place(relx=0.3, rely=self.buttonPlacey, relwidth=0.1, relheight=0.05)
        self.addButton = tk.Button(self.canvas, text="Add", command=self.add)
        self.addButton.place(relx=0.6, rely=self.buttonPlacey, relwidth=0.1, relheight=0.05)
        self.removeButton = tk.Button(self.canvas, text="Remove", command=self.remove)
        self.removeButton.place(relx=0.8, rely=self.buttonPlacey, relwidth=0.1, relheight=0.05)
        self.playButton = tk.Button(self.canvas, text="Play", command=self.play)
        self.playButton.place(relx=0.7, rely=0.85, relwidth=0.1, relheight=0.1)
        self.setBreakButton = tk.Button(self.canvas, text="Set Break", command=self.setBreak)
        self.setBreakButton.place(relx=0.25, rely=0.85, relwidth=0.1, relheight=0.05)


        # Video Canvas
        self.exVidCanvas = tk.Canvas(self.canvas, bg='lightblue')
        self.exVidScrollbar = ttk.Scrollbar(self.canvas, orient="vertical", command=self.exVidCanvas.yview)
        self.exVidFrame = ttk.Frame(self.exVidCanvas)

        # This handles when the box changes in size due to increase in videos
        self.exVidFrame.bind(
            "<Configure>",
            lambda e: self.exVidCanvas.configure(
                scrollregion=self.exVidCanvas.bbox("all")
            )
        )

        self.exVidCanvas.create_window((0, 0), window=self.exVidFrame, anchor="nw")
        self.exVidCanvas.configure(yscrollcommand=self.exVidScrollbar.set)

        self.exVidCanvas.place(relx=0, rely=self.windowPlacey, relwidth=0.5, relheight=self.windowHeight)
        self.exVidScrollbar.place(relx=0.5, rely=self.windowPlacey, relheight=self.windowHeight, anchor='ne')


        # Workout Canvas
        self.workoutCanvas = tk.Canvas(self.canvas, bg='lightgreen')
        self.workoutScrollbar = ttk.Scrollbar(self.canvas, orient="vertical", command=self.workoutCanvas.yview)
        self.workoutFrame = ttk.Frame(self.workoutCanvas)

        # This handles when the box changes in size due to increase in videos
        self.workoutFrame.bind(
            "<Configure>",
            lambda e: self.workoutCanvas.configure(
                scrollregion=self.workoutCanvas.bbox("all")
            )
        )

        self.workoutCanvas.create_window((0, 0), window=self.workoutFrame, anchor="nw")
        self.workoutCanvas.configure(yscrollcommand=self.workoutScrollbar.set)

        self.workoutCanvas.place(relx=0.5, rely=self.windowPlacey, relwidth=0.5, relheight=self.windowHeight)
        self.workoutScrollbar.place(relx=1, rely=self.windowPlacey, relheight=self.windowHeight, anchor='ne')

    # Upload button functions
    def upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
        if file_path:
            output_path = file_path.replace(".mp4", "_processed.mp4") # This creates the output path for use in processing the video and add _process onto the end to differentiate the video
            angles_output_path = file_path.replace(".mp4", "_angles.json") # This should create a Json file and an output path leadin to that json file
            processed_video = self.processVideo(file_path, output_path, angles_output_path)
            self.addThumbnail(output_path, angles_output_path)

    def processVideo(self, video_path, output_path, angles_output_path):
        try:
            processedVideo = videoPose(video_path, output_path, angles_output_path)
            processedVideo.drawPose()
            return processedVideo
        except:
            print("error processing video") 
            return None

    def getThumbnail(self, video_path):
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (120, 90))  # Resize to thumbnail size 120, 90
            image = Image.fromarray(frame)
            return ImageTk.PhotoImage(image)
        cap.release()
        return None
    
    def addThumbnail(self, video_path, angles_path):
        thumbnail = self.getThumbnail(video_path)
        label = tk.Label(self.exVidFrame, bg="lightgreen", image=thumbnail)
        label.image = thumbnail  # Keep a reference to avoid garbage collection, python may delete the image without a reference
        label.video_path = video_path # Store the video path in the thumbnail
        label.angles_path = angles_path # Store the angles in the thumbnail
        label.pack(padx=10, pady=10)
        label.bind("<Button-1>", lambda e: self.selectThumbnail(label))
        label.bind("<Button-3>", lambda e: self.playVideo(label.video_path))

    # Thumbnail functions
    def selectThumbnail(self, label):
        self.selected_thumbnail = label
        self.selected_thumbnail.config(borderwidth=2, relief="solid")

    def playVideo(self, video_path):
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Video', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

    # Remaining buttons
    def delete(self):
        if self.selected_thumbnail:
            video_path = self.selected_thumbnail.video_path
            angles_path = self.selected_thumbnail.angles_path
            self.selected_thumbnail.destroy()
            self.selected_thumbnail = None
            try:
                os.remove(video_path)
            except:
                print("error deleting video path")

            try:
                os.remove(angles_path)
            except:
                print("error deleting angles file")

    def add(self):
        if self.selected_thumbnail:
            new_label = tk.Label(self.workoutFrame, image=self.selected_thumbnail.image)
            new_label.image = self.selected_thumbnail.image  # Keep a reference to avoid garbage collection
            new_label.video_path = self.selected_thumbnail.video_path  # Store the video path in the new thumbnail
            new_label.angles_path = self.selected_thumbnail.angles_path # Store the angles in the thumbnail
            new_label.pack(padx=10, pady=10)
            new_label.bind("<Button-1>", lambda e: self.selectThumbnail(new_label))
            new_label.bind("<Button-3>", lambda e: self.playVideo(new_label.video_path))
            self.selected_thumbnail.destroy()
            self.selected_thumbnail = None

    def remove(self):
        if self.selected_thumbnail:
            new_label = tk.Label(self.exVidFrame, image=self.selected_thumbnail.image)
            new_label.image = self.selected_thumbnail.image  # Keep a reference to avoid garbage collection
            new_label.video_path = self.selected_thumbnail.video_path  # Store the video path in the new thumbnail
            new_label.angles_path = self.selected_thumbnail.angles_path # Store the angles in the thumbnail
            new_label.pack(padx=10, pady=10)
            new_label.bind("<Button-1>", lambda e: self.selectThumbnail(new_label))
            new_label.bind("<Button-3>", lambda e: self.playVideo(new_label.video_path))
            self.selected_thumbnail.destroy()
            self.selected_thumbnail = None

    def setBreak(self):
        try:
            time = int(self.breakEntry.get())
            mins, secs = divmod(time, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            self.breakTime.config(text=f"{time_format}")
        except:
            messagebox.showerror("Invalid input", "Invalid text format")


    # Functions for switching canvas
    def play(self):
        video_paths = [label.video_path for label in self.workoutFrame.winfo_children()]
        angles_paths = [label.angles_path for label in self.workoutFrame.winfo_children()]
        time = self.breakTime.cget("text")
        minutes, seconds = map(int, time.split(":"))
        break_time = minutes * 60 + seconds
        self.root.withdraw()  # Hide the current window
        new_root = tk.Toplevel(self.root, height=1000, width=800)
        PlayFrame(new_root, self.root, video_paths, angles_paths, break_time)









class PlayFrame:
    def __init__(self, root, main_frame, video_paths, angles_paths, break_time):
        self.root = root
        self.main_frame = main_frame
        self.video_paths = video_paths
        self.angles_paths = angles_paths
        self.break_time = break_time

        self.cvHeight = 400
        self.cvWidth = 600

        self.differenceThreshold = 5

        self.points = 100

        #Initialise angles dict to be filled with angles each frame and the index of the angles list being read
        self.video_angles = {}
        self.angles_idx = 0

        # Create Base canvas layer
        self.root.title("Results")
        self.canvas = tk.Canvas(self.root, width=1000, height=800, bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        self.ResultsText = tk.Label(self.canvas, text="Results")
        self.ResultsText.place(relx=0.45, rely=0.2, relwidth=0.1, relheight=0.1)

        self.backButton = tk.Button(self.canvas, text="Back", command=self.back)
        self.backButton.place(relx=0.45, rely=0.4, relwidth=0.1, relheight=0.1)

        self.playWorkout(self.break_time)


    def playWorkout(self, break_time):
        live_pose = livePose()

        self.createCountdown(5, live_pose)

        for video_path in self.video_paths:
            for angles_path in self.angles_paths:
                self.startVideoandLive(live_pose, video_path, angles_path, break_time)

    # Angles path should now be fed here, so all i need to do now
    # is use the angles path and the method in livepose to get live
    # angles and compare the two
    def startVideoandLive(self, live_pose, video_path, angles_path, break_time):
        # Load list of video angle dicts
        angles_list = self.loadAngles(angles_path)

        vid = cv2.VideoCapture(video_path)

        if not vid.isOpened():
            print(f"Error: Cannot open video file {video_path}")
            return
        
        live_pose.cap = cv2.VideoCapture(0)
        while live_pose.cap.isOpened() and vid.isOpened():
            vid_ret, vid_frame = vid.read()

            # Set the video angles dict to the next frame of angles
            self.video_angles = angles_list[self.angles_idx]
            self.angles_idx += 1

            # Stop if video or live feed fail
            if not vid_ret:
                print("Error: Could not read frame from video.")
                break

            # Process live frame
            image = live_pose.drawPose()

            if image is None:
                print("Error: No frame captured from live feed.")
                break

            # Resize frames
            try:
                image = cv2.resize(image, (self.cvWidth, self.cvHeight))
                vid_frame = cv2.resize(vid_frame, (self.cvWidth, self.cvHeight))
            except cv2.error as e:
                print(f"Error during resizing: {e}")
                break

            # Combine the frames
            combined_frame = cv2.vconcat([image, vid_frame])
            cv2.imshow('Combined Feed', combined_frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            # Compare angles from live and video frame
            self.compareAngles(live_pose.angles, self.video_angles)
        
        self.createCountdown(break_time, live_pose)

        vid.release()
        live_pose.cap.release()


    def createCountdown(self, time, live_pose):
        fps = 30

        for t in range(time*fps, -1, -1):
            # Create black image
            cap_frame = live_pose.drawPose()
            cap_frame = cv2.resize(cap_frame, (self.cvWidth, self.cvHeight))
            vid_frame = np.zeros((self.cvHeight, self.cvWidth, 3), dtype=np.uint8)

            # Display countdown timer
            # Change this so the number only updates at each second
            time_sec = t//30
            minutes, seconds = divmod(time_sec, 60)
            timer_str = f"{minutes:02}:{seconds:02}"
            cv2.putText(vid_frame, timer_str, (self.cvWidth // 2 - 50, self.cvHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 4, cv2.LINE_AA)
            # Really odd but the text is placed in a weird position so //2-50 is required to move it in place

            # Combine the frames
            combined_frame = cv2.vconcat([cap_frame, vid_frame])

            # Show the frame multiple times to achieve the desired duration
            #for _ in range(fps):
            cv2.imshow('Combined Feed', combined_frame)
            if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
                break

    
    # New function to do countdown with the points labelled (for the second countdown after an exercise)
    def createCountdownPoints(self, time, live_pose, points):
        fps = 30

        for t in range(time*fps, -1, -1):
            # Create black image
            cap_frame = live_pose.drawPose()
            cap_frame = cv2.resize(cap_frame, (self.cvWidth, self.cvHeight))
            vid_frame = np.zeros((self.cvHeight, self.cvWidth, 3), dtype=np.uint8)

            # Display countdown timer
            # Change this so the number only updates at each second
            time_sec = t//30
            minutes, seconds = divmod(time_sec, 60)
            timer_str = f"{minutes:02}:{seconds:02}"
            cv2.putText(vid_frame, timer_str, (self.cvWidth // 2 - 50, self.cvHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 4, cv2.LINE_AA)
            cv2.putText(vid_frame, points, (self.cvWidth // 2 - 50, self.cvHeight // 2), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 4, cv2.LINE_AA)

            # Combine the frames
            combined_frame = cv2.vconcat([cap_frame, vid_frame])

            # Show the frame multiple times to achieve the desired duration
            #for _ in range(fps):
            cv2.imshow('Combined Feed', combined_frame)
            if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
                break

    # Open json file
    def loadAngles(self, angles_path):
        with open(angles_path, 'r') as f:
            angles_list = json.load(f)
        return angles_list
    
    # Points System
    # This compares single set of live and video angles
    def compareAngles(self, live_angles, video_angles):
        # Compare angles between live and video
        for key in live_angles:
            live_angle = live_angles.get(key)
            video_angle = video_angles.get(key)
            
            if live_angle is None or video_angle is None:
                print(f"Angle at {key} could not be calculated in one of the feeds.")
            else:
                difference = abs(live_angle - video_angle)
                print(f"Angle difference at {key}: {difference}")
                if difference > self.differenceThreshold:
                    self.points -= 1
                    # Have to minus 100 if they dont perform the exercise right? so how do i do the math
                    # 100/(30*time)
                    # Problem is this time is determined by how long the video is, need the info from the video_path somehow
                # Add of statement, takes away a point every 100ms if the angle difference is greater than 2 or something

    def back(self):
        self.root.withdraw()
        self.main_frame.deiconify()


# Test
testroot = tk.Tk()

Test = MainFrame(testroot)

testroot.mainloop()