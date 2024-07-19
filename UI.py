import tkinter as tk
import cv2

class MainFrame:
    def __init__(self, root):
        self.root = root

        # Create Base canvas layer
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)



class ExvidFrame:
    def __init__(self, root, videos):
        self.root = root

        self.frame = tk.Frame(self)

class WorkoutFrame:
    def __init__(self, root, videos):
        self.root = root

        self.frame = tk.Frame(self)



# Test
testroot = tk.Tk()
Test = MainFrame(testroot)