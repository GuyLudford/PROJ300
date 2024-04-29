import cv2
import numpy as np

# Load your climbing wall image
image_path = "Blank Wall.jpg"
image = cv2.imread(image_path)

# Preprocessing: Convert to grayscale and apply thresholding
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out small contours (adjust the threshold as needed)
min_contour_area = 10
valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

# Draw bounding boxes around detected holds
for cnt in valid_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the result
cv2.imshow("Detected Holds", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
