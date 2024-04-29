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

    # Merge nearby contours into larger bounding boxes
    merged_contours = []
    for cnt in valid_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        merged_contours.append((x, y, x + w, y + h))

    # Group overlapping bounding boxes
    grouped_contours = []
    while merged_contours:
        current_box = merged_contours.pop(0)
        x1, y1, x2, y2 = current_box
        for other_box in merged_contours[:]:
            ox1, oy1, ox2, oy2 = other_box
            if (x1 <= ox2 and x2 >= ox1) and (y1 <= oy2 and y2 >= oy1):
                # Overlapping boxes, merge them
                x1 = min(x1, ox1)
                y1 = min(y1, oy1)
                x2 = max(x2, ox2)
                y2 = max(y2, oy2)
                merged_contours.remove(other_box)
        grouped_contours.append((x1, y1, x2, y2))

    # Draw merged bounding boxes on the image
    for x1, y1, x2, y2 in grouped_contours:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Save the modified image
cv2.imwrite('Detected_Objects_Merged.jpg', image)

# Display the image with bounding boxes
cv2.imshow('Detected Objects', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
