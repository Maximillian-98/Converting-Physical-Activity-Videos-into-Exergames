import tkinter as tk
from tkinter import ttk
import cv2

class MainFrame:
    def __init__(self, root):
        self.root = root

        # Create Base canvas layer
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        # Scrollable frames for videos and workout
        self.exVidCanvas = tk.Canvas(self.canvas, bg='lightblue')
        self.exVidScrollbar = ttk.Scrollbar(self.canvas, orient="vertical", command=self.exVidCanvas.yview)
        self.exVidFrame = ttk.Frame(self.exVidCanvas)

        self.exVidFrame.bind(
            "<Configure>",
            lambda e: self.exVidCanvas.configure(
                scrollregion=self.exVidCanvas.bbox("all")
            )
        )

        self.exVidCanvas.create_window((0, 0), window=self.exVidFrame, anchor="nw")
        self.exVidCanvas.configure(yscrollcommand=self.exVidScrollbar.set)

        self.exVidCanvas.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        self.exVidScrollbar.place(relx=0.5, rely=0, relheight=1, anchor='ne')


        self.workoutFrame = tk.Frame(self.canvas)
        self.workoutFrame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)





class PlayFrame:
    def __init__(self, root):
        self.root = root




# Test
testroot = tk.Tk()
Test = MainFrame(testroot)

testroot.mainloop()