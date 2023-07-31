import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
count = 1
while True:
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh = cv2.threshold(delta_frame, thresh=13, maxval=255, type=cv2.THRESH_BINARY)[1]

    # increase the size and thickness of the foreground image or to connect broken pieces of an object
    dil_thresh = cv2.dilate(src=thresh, kernel=None, iterations=1)

    # cv2.imshow("My Video", dil_thresh)

    contours, hierarchy = cv2.findContours(image=dil_thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    # iterating over the list of contours provided stored in the contours of the cv2.findContours
    for contour in contours:
        # if this is a small object area, it should be ignored
        if cv2.contourArea(contour) < 5000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow("Object Detection", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break


video.release()
