# Converting Physical Activity Videos into Exergames
This project is a proof of concept application that allows for the upload of video workout exercises to create a gamified workout that offers points and a leaderboard system for comparison of high scores

## Running the Code
The code can be ran simply by running UI.py. The required packages of this code are tkinter, MediaPipe and OpenCV.

## UI Explanation
Upon startup, the UI presented allows for the upload of videos, These videos must be cropped beforehand to include only the desired exercise. After upload, selecting a video and pressing add will add the video to the workout tab, all videos in this tabe will play in order from top to bottom when the play button is pressed, with a five second countdown before the workout and a break countdown that is also set on this same screen.


## Current Issues
Unfortunately I was not able to fix a frustratingly simple bug with the upload feature. When a vidoe is uploaded the user must press 'q' before the end of the video for it to properly upload. My current understanding is that this breaks the loop early allowing for proper upload since the final frames of a video seem to break the upload feature.