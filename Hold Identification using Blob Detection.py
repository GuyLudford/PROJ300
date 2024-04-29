import cv2
import numpy as np

# Load the image
image_path = 'Blank Wall.jpg'
original_image = cv2.imread(image_path)

# Convert to grayscale
gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray_image, 100, 200)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours by area and shape
filtered_contours = []
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 50:  # Adjust this threshold as needed
        filtered_contours.append(contour)

# Draw bounding boxes on the original image
for contour in filtered_contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green bounding box

# Display the result
cv2.imshow('Bounding Boxes', original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
