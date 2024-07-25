import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk # For getting image for thumbnail
from main import videoPose
import os

class MainFrame:
    def __init__(self, root):
        self.root = root
        self.root.title("to be named")

        self.windowPlacey = 0.1
        self.windowHeight = 0.65
        self.buttonPlacey = 0.75


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
            processed_video = self.processVideo(file_path, output_path)
            self.addThumbnail(output_path)

    def processVideo(self, video_path, output_path):
        try:
            processedVideo = videoPose(video_path, output_path)
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
            frame = cv2.resize(frame, (120, 90))  # Resize to thumbnail size
            image = Image.fromarray(frame)
            return ImageTk.PhotoImage(image)
        cap.release()
        return None
    
    def addThumbnail(self, video_path):
        thumbnail = self.getThumbnail(video_path)
        label = tk.Label(self.exVidFrame, bg="lightgreen", image=thumbnail)
        label.image = thumbnail  # Keep a reference to avoid garbage collection, python may delete the image without a reference
        label.video_path = video_path # Store the video path in the thumbnail
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
            self.selected_thumbnail.destroy()
            self.selected_thumbnail = None
            try:
                os.remove(video_path)
            except:
                print("error deleting video path")

    def add(self):
        if self.selected_thumbnail:
            new_label = tk.Label(self.workoutFrame, image=self.selected_thumbnail.image)
            new_label.image = self.selected_thumbnail.image  # Keep a reference to avoid garbage collection
            new_label.video_path = self.selected_thumbnail.video_path  # Store the video path in the new thumbnail
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
        time = self.breakTime.cget("text")
        minutes, seconds = map(int, time.split(":"))
        break_time = minutes * 60 + seconds
        self.root.withdraw()  # Hide the current window
        new_root = tk.Toplevel(self.root, height=1000, width=800)
        PlayFrame(new_root, self.root, video_paths, break_time)









class PlayFrame:
    def __init__(self, root, main_frame, video_paths, break_time):
        self.root = root
        self.main_frame = main_frame
        self.video_paths = video_paths
        self.break_time = break_time

        # Create Base canvas layer
        self.root.title("Workout")
        self.canvas = tk.Canvas(self.root, width=1000, height=800, bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        # Canvas for video and break text
        self.vidCanvas = tk.Canvas(self.canvas, bg='lightblue')
        self.vidFrame = ttk.Frame(self.vidCanvas)
        self.vidCanvas.create_window((0, 0), window=self.vidFrame, anchor="nw")
        self.vidCanvas.place(relx=0, rely=0, relwidth=1, relheight=0.5)

        self.breakText = tk.Label(self.vidCanvas, text="00:00")
        self.breakText.place(relx=0.4, rely=0.4, relwidth=0.1, relheight=0.05)

        # Canvas for live feed
        self.liveFeedCanvas = tk.Canvas(self.canvas, bg='lightgreen')
        self.liveFeedFrame = ttk.Frame(self.liveFeedCanvas)
        self.liveFeedCanvas.create_window((0, 0), window=self.liveFeedFrame, anchor="nw")
        self.liveFeedCanvas.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

        self.backButton = tk.Button(self.canvas, text="Back", command=self.back)
        self.backButton.place(relx=0.4, rely=0.8, relwidth=0.1, relheight=0.05)


    def playWorkout(self, break_time):
        for video_path in self.video_paths:
            self.playVideo(video_path)
            self.breakTime(break_time)

    #def startLiveFeed(self):
    #    liveFeed = livePose()
    #    liveFeed.drawPose()

    # Might have to change this to the dual thing that jim did in his thing
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


    def breakTime(self, break_time):
        if break_time > 0:
            minutes, seconds = divmod(break_time, 60)
            time_str = f"{minutes:02}:{seconds:02}"
            self.breakText.config(text=time_str)
            # Call this function again after 1 second (1000 ms)
            self.root.after(1000, self.breakTime, break_time - 1)
        else:
            self.breakText.config(text="")


    def back(self):
        self.canvas.destroy()
        self.canvas.master.deiconify()





# Test
testroot = tk.Tk()

Test = MainFrame(testroot)

testroot.mainloop()