# pip install https://github.com/Khang-NT/youtube-dl/archive/master.zip
# will fix cv2 error


import vlc
import pafy
import os
import time
from cv2 import cv2

# Constants (might need to change)
link = 'https://www.youtube.com/watch?v=r4MwfNzUq9k'
tempDirectory = 'temp/'

# Make temporary directory for screenshots
try:
    os.mkdir(tempDirectory)
except:
    pass

url = link.split("=")[1]
vid = pafy.new(url)
print("Scanning video:", vid.title, "\n")

dl = vid.getbest(preftype='mp4')
filename = dl.download(tempDirectory)
os.rename(filename, tempDirectory + url + '.mp4')
filename = tempDirectory + url + '.mp4'

# OpenCV
first = None

capture = cv2.VideoCapture(filename)

if (capture.isOpened() == False):
    print("Erorr: Cannot open video")

# Read until video is completed
while(capture.isOpened()):
  # Capture frame-by-frame
  ret, frame = capture.read()
  if ret == True:
 
    curFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    curFrame = cv2.GaussianBlur(curFrame, (21, 21), 0)

    if first is None:
        first = curFrame
        continue
    
    delta_frame = cv2.absdiff(first, curFrame)
    threshold_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    threshold_delta = cv2.dilate(threshold_delta, None, iterations=0)
    (_,cnts,_) = cv2.findContours(threshold_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # When PDF is scrolled, frame to compare to is reset
    # This is to ensure only the moving slider is picked up
    if (len(cnts) > 100):
        first = curFrame
        continue

    for contour in cnts:
        if cv2.contourArea(contour) < 300:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 3)

    # cv2.imshow('frame', frame)
    # cv2.imshow('Capturing', gray)
    # cv2.imshow('delta', delta_frame)
    # cv2.imshow('thresh', threshold_delta)

    # Display the resulting frame
    cv2.imshow('Frame',frame)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
capture.release()
 
# Closes all the frames
cv2.destroyAllWindows()

# Remove temp folder
if os.path.isdir(tempDirectory):
    os.rmdir(tempDirectory)

# For screenshots
# Player.video_take_snapshot(0, directory + str(t) + ".png", 0, 0) 