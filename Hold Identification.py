import cv2
import numpy as np

# Load your image
image = cv2.imread('Blank Wall.jpg')

# Convert to HSV
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
h, _, _ = cv2.split(image_hsv)

# Apply K-means clustering
K = 6  # Number of clusters (adjust as needed)
samples = h.reshape(-1, 1).astype(np.float32)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
_, labels, centers = cv2.kmeans(samples, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Create masks for each cluster center
for center in centers:
    hue_value = int(center[0])
    lower_bound = np.array([hue_value - 10, 50, 50])
    upper_bound = np.array([hue_value + 10, 255, 255])
    mask = cv2.inRange(image_hsv, lower_bound, upper_bound)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours (adjust the threshold as needed)
    min_contour_area = 60
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    for cnt in valid_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(f"Object at ({x}, {y}), Hue: {hue_value}")

# Display the image with bounding boxes
cv2.imshow('Detected Objects', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
