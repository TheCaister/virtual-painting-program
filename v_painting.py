import cv2

# Setting width and height of webcam window
frameWidth = 640
frameHeight = 480

# Displaying a webcam
cap = cv2.VideoCapture(0)
# In set(), the first parameter is the ID of the property to change
# In this case, we're setting the width, height and brightness of the image
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

# Infinite loop for displaying frames captured by webcam
while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    # If Q is pressed, quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
