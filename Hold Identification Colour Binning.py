import cv2
import numpy as np

# Load the image
image_path = 'Blank Wall.jpg'
original_image = cv2.imread(image_path)

# Convert to HSV
image_hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
h, _, _ = cv2.split(image_hsv)

# Create a histogram of hue values
bins = np.bincount(h.flatten())

# Set a threshold for dominant hues (adjust as needed)
MIN_PIXEL_CNT_PCT = 1.0 / 20.0
peaks = np.where(bins > (h.size * MIN_PIXEL_CNT_PCT))[0]

# Create masks for each dominant hue
masks = []
for peak in peaks:
    lower_bound = max(0, peak - 10)  # Adjust the range as needed
    upper_bound = min(180, peak + 10)
    mask = cv2.inRange(h, lower_bound, upper_bound)
    masks.append(mask)

# Find contours and draw bounding boxes
for mask in masks:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green bounding box

# Display the result
cv2.imshow('Color Bounding Boxes', original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
