import os
import cv2
import time
from emailing import send_email
import glob
import cleanImageFolder
from threading import Thread


cleanImageFolder.cleanImgFolder()

video = cv2.VideoCapture(1)
time.sleep(5)
first_frame = None
status_list = []
count = 1
while True:
    # read frame from VideoCapture
    status = 0
    check, frame = video.read()

    # reduce the details of the images for easy detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # compare the first frame to the next ones
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh = cv2.threshold(delta_frame, thresh=30, maxval=255, type=cv2.THRESH_BINARY)[1]

    # increase the size and thickness of the foreground image or to connect broken pieces of an object
    dil_thresh = cv2.dilate(src=thresh, kernel=None, iterations=2)

    # cv2.imshow("My Video", dil_thresh)

    contours, hierarchy = cv2.findContours(image=dil_thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    # iterating over the list of contours provided stored in the contours of the cv2.findContours
    for contour in contours:
        # if this is a small object area, it should be ignored
        if cv2.contourArea(contour) < 5000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if rectangle.any:
            img = cv2.imwrite(f'images/{count}.png', frame)
            count = count + 1

            img_len = glob.glob("images/*png")
            index = int(len(img_len)/2)
            obj_index = f'images/{index}.png'
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]

    print(status_list)

    if status_list[0] == 1 and status_list[1] == 0:
        print("Hello World")
        email_thread = Thread(target=send_email, args=(obj_index, ))
        email_thread.daemon = True
        email_thread.start()
        count = 1

    cv2.imshow("Object Detection", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
