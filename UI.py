import tkinter as tk
import cv2

class MainFrame:
    def __init__(self, root):
        self.root = root

        # Create Base canvas layer
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        self.Exvidframe = tk.Frame(self.canvas)
        self.ExvidFrame.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        self.Workoutframe = tk.Frame(self.canvas)
        self.WorkoutFrame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)





class PlayFrame:
    def __init__(self, root):
        self.root = root




# Test
testroot = tk.Tk()
Test = MainFrame(testroot)