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

# List of colours to detect
myColors = [
    # Orange, purple and green
    [6, 166, 167, 17, 255, 255],
    [29, 124, 125, 179, 231, 255],
    [59, 54, 7, 83, 132, 255]
]

# Color values that correspond to the color detected
myColorValues = [
    [51, 153, 255],
    [255, 0, 255],
    [0, 255, 0]
]

# Keep track of all the points to be drawn. Each value follows the form:
# [x, y, colorID]
myPoints = []


def findColor(img, colors, color_values):
    # Convert frames to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Keep track of which color value we are on
    count = 0

    newPoints = []

    # Creating a mask to filter out stuff
    # The first 3 elements of the colour is the lower bound
    # The second 3 elements is the upper bound
    # Create mask for each color in the list of colours passed
    for color in colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        # Get the top center of the mask
        x, y = getContours(mask)
        # Draw on this point a circle
        cv2.circle(imgResult, (x, y), 10, color_values[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]), mask)

    return newPoints


def getContours(img):
    # Use the findContours function, passing in RETR_EXTERNAL which returns the extreme outer contours
    # Passing in CHAIN_APPROX_NONE means we'll get ALL the contours. No compressed values
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Setting default values in case area is less than 500
    x, y, w, h = 0, 0, 0, 0

    # Iterate through every contour and find their areas
    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Make sure the areas are above a certain value to reduce noise
        if area > 500:
            # -1 for contour index means that we want to draw EVERY contour
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)

            # Getting the perimeters of every contour, passing in True because they're all closed
            perimeter = cv2.arcLength(cnt, True)

            # Create a rough polygon based on the contours
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)

            # Getting bounding boxes for every approximate polygon then drawing them out
            x, y, w, h = cv2.boundingRect(approx)

    # Returning the top center of the bounding box
    # return x + w // 2, y
    return x, y + h // 2


def drawOnCanvas(points, values):
    for point in points:
        cv2.circle(imgResult, (point[0], point[1]), 10, values[point[2]], cv2.FILLED)


# Infinite loop for displaying frames captured by webcam
while True:
    success, img = cap.read()
    # Create a copy to be drawn on
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)

    if len(newPoints) != 0:
        for point in newPoints:
            myPoints.append(point)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)


    # Rotating the webcam for my particular device
    cv2.imshow("Video", cv2.rotate(imgResult, cv2.ROTATE_90_CLOCKWISE))
    # If Q is pressed, quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
