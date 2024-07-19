import tkinter as tk
from tkinter import ttk
import cv2

class MainFrame:
    def __init__(self, root):
        self.root = root
        self.root.title("to be named")

        self.windowHeight = 0.5

        # Create Base canvas layer
        self.canvas = tk.Canvas(self.root, width=1000, height=800, bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)


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

        self.exVidCanvas.place(relx=0, rely=0, relwidth=0.5, relheight=self.windowHeight)
        self.exVidScrollbar.place(relx=0.5, rely=0, relheight=self.windowHeight, anchor='ne')


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

        self.workoutCanvas.place(relx=0.5, rely=0, relwidth=0.5, relheight=self.windowHeight)
        self.workoutScrollbar.place(relx=1, rely=0, relheight=self.windowHeight, anchor='ne')





class PlayFrame:
    def __init__(self, root):
        self.root = root




# Test
testroot = tk.Tk()

Test = MainFrame(testroot)

testroot.mainloop()