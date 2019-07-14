# pip install https://github.com/Khang-NT/youtube-dl/archive/master.zip
# will fix cv2 error

import pafy
import os
import time
from cv2 import cv2
import shutil

# Constants (might need to change)
link = 'https://www.youtube.com/watch?v=r4MwfNzUq9k'
# link = 'https://www.youtube.com/watch?v=YEEbpwP9cTw'
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

# Array to store the 3 most recent X values of the bar moving across the notes
bar_x = []

# Read until video is completed
while(capture.isOpened()):
  # Capture frame-by-frame
  ret, frame = capture.read()
  if ret == True:
    cur_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if first is None:
        first = cur_frame
        continue
    
    delta_frame = cv2.subtract(first, cur_frame)
    threshold_delta = cv2.threshold(delta_frame, 20, 255, cv2.THRESH_BINARY)[1]
    (_,cnts,_) = cv2.findContours(threshold_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # When PDF is scrolled, frame to compare to is reset
    # This is to ensure only the moving slider is picked up
    if (len(cnts) > 100):
        first = cur_frame
        # time.sleep(5000)
        continue

    count = 0
    tallest = -1
    tallest_x = -1
    # tallest_contour = cnts[0]
    for contour in cnts:
        if cv2.contourArea(contour) < 70:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 3)

        if h > tallest:
            tallest = h
            tallest_contour = contour
            tallest_x = x
            
        cv2.putText(frame, str(y), (30, 60 + count*60), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
        count += 1

    # If there is a large enough gap between X values, detect a new line
    if bar_x and tallest_x != -1 and bar_x[0] != -1 and abs(tallest_x - bar_x[0]) > 200:
        print("NEW LINE")
        first = cur_frame
        bar_x = []

    # Update the x values
    if len(bar_x) > 3:
        bar_x.pop(0)
    bar_x.append(tallest_x)

    # cv2.imshow('Capturing', cur_frame)
    cv2.imshow('Frame',frame)
    cv2.imshow('delta', delta_frame)
    cv2.imshow('thresh', threshold_delta)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  else: 
    break
 
# When everything done, release the video capture object
capture.release()
 
# Closes all the frames
cv2.destroyAllWindows()

# Remove temp folder
if os.path.isdir(tempDirectory):
    shutil.rmtree(tempDirectory)

# For screenshots
# Player.video_take_snapshot(0, directory + str(t) + ".png", 0, 0) 