# pip install https://github.com/Khang-NT/youtube-dl/archive/master.zip
# will fix cv2 error

import pafy
import os
import time
from cv2 import cv2
from fpdf import FPDF
import shutil

PDF_WIDTH = 210
PDF_HEIGHT = 297

# Convert list of images (1 for each line of music) into a PDF
def imgsToPDF(fileName, imgList, dir = ''):
    pdf = FPDF()
    pdf.add_page()

    mm_multiplier = 0.264583333 # FPDF works in millimeters
    curH = 0
    for img in imgList:
        # print(img)
        cvImg = cv2.imread(img)

        height, width, channels = cvImg.shape
        height *= mm_multiplier
        width *= mm_multiplier

        new_width = PDF_WIDTH
        new_height = (new_width * height) / width

        if curH + new_height + 2 > PDF_HEIGHT:
            pdf.add_page()
            curH = 0

        pdf.image(img, x=0, y=curH, w=new_width, h=new_height)
        curH = curH + new_height + 2

    pdf.output(dir + fileName + ".pdf", "F")
    print("PDF created with name " + fileName + ".pdf")

# Crop the current frame and save it in given directory
def saveLine(frame, frames, dir = '', firstLine = False):
    height, width, channels = frame.shape

    if firstLine:
        cropped_img = frame[0:y_upperbound, 0:width]
    else:
        cropped_img = frame[y_lowerbound:y_upperbound, 0:width]
    # cv2.imshow("frame%d" % frames, cropped_img)
    cv2.imwrite(dir + "frame%d.png" % frames, cropped_img)
    imgList.append(dir + "frame%d.png" % frames)

# # Constants (might need to change)
link = 'https://www.youtube.com/watch?v=r4MwfNzUq9k'
# # link = 'https://www.youtube.com/watch?v=YEEbpwP9cTw'
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
    print("Error: Cannot open video")

# Array to store the 5 most recent X values of the bar moving across the notes
bar_x = []

# Read until video is completed
first_frame = True
frames = 0
imgList = []
while(capture.isOpened()):
    # Capture frame-by-frame
    ret, frame = capture.read()
    frames += 1

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
            continue

        # count = 0
        tallest = -1
        tallest_x = -1

        y_upperbound = -1
        y_lowerbound = float('inf')

        for contour in cnts:
            # Should have option to change this tolerance as it causes some videos to break
            if cv2.contourArea(contour) < 70:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(cur_frame, (x,y), (x+w, y+h), (255, 0, 0), 3)

            if y+h > y_upperbound:
                y_upperbound = y+h
            if y < y_lowerbound:
                y_lowerbound = y

            if h > tallest:
                tallest = h
                tallest_contour = contour
                tallest_x = x

            # For debugging
            # cv2.putText(cur_frame, str(y), (30, 60 + count*60), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
            # count += 1

        # If there is a large enough gap between X values, detect a new line
        prevTrue = False
        for x in bar_x:
            if frames == 35 and first_frame and y_upperbound != -1:
                if prevTrue:
                    saveLine(frame, frames, tempDirectory, True)
                    break
                prevTrue = True

            if tallest_x != -1 and x != -1 and abs(tallest_x - x) > 200:
                if prevTrue:
                    saveLine(frame, frames, tempDirectory)
                    first = cur_frame
                    bar_x = []
                    break
                prevTrue = True

        # Update the x values
        if len(bar_x) > 5:
            bar_x.pop(0)
        bar_x.append(tallest_x)

        cv2.imshow('Frame', frame)
        cv2.imshow('Cur frame', cur_frame)
        cv2.imshow('Delta', delta_frame)
        cv2.imshow('Thresh', threshold_delta)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    else:
        break
 
# When everything done, release the video capture object
capture.release()
 
# Closes all the frames
cv2.destroyAllWindows()

# Turn series of images into a PDF
imgsToPDF(vid.title, imgList)

# Remove temp folder
# if os.path.isdir(tempDirectory):
    # shutil.rmtree(tempDirectory)
