import cv2.cv2 as cv2
import numpy as np

# Setting width and height of webcam window
frameWidth = 640
frameHeight = 480

# Displaying a webcam
cap = cv2.VideoCapture(0)
# In set(), the first parameter is the ID of the property to change
# In this case, we're setting the width, height and brightness of the image
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)


def empty(a):
    pass


# Creating a window named trackbars, resizing it
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
# Create several bars for adjusting stuff
# Need name of value, name of window, min and max values, and a function to call(empty function in our case)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 154, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 58, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 130, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

# while True to make live updates to the image.
while True:
    success, img = cap.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Getting trackbar position of trackbars
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min, s_min, v_min, h_max, s_max, v_max)

    # Creating a mask to filter out stuff
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)

    # Doing an AND operation using the mask to extract only the color we need
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hstack = np.hstack([img, mask, imgResult])

    cv2.imshow("Stacking", hstack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
