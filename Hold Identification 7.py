import cv2
import numpy as np

def merge_boxes(boxes, x_val, y_val):
    merged_boxes = []
    while len(boxes) > 0:
        current_box = boxes.pop(0)
        x1, y1, w1, h1 = current_box
        merged_box = current_box

        for box in boxes:
            x2, y2, w2, h2 = box
            if abs(x1 - x2) < x_val and abs(y1 - y2) < y_val:
                # Merge boxes
                x_min = min(x1, x2)
                y_min = min(y1, y2)
                x_max = max(x1 + w1, x2 + w2)
                y_max = max(y1 + h1, y2 + h2)
                merged_box = (x_min, y_min, x_max - x_min, y_max - y_min)
                break

        merged_boxes.append(merged_box)

    return merged_boxes

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

    # Get bounding boxes
    boxes = [cv2.boundingRect(cnt) for cnt in valid_contours]
    # Merge nearby bounding boxes
    merged_boxes = merge_boxes(boxes, x_val=150, y_val=150)

    for x, y, w, h in merged_boxes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(f"Merged box at ({x}, {y}), Width: {w}, Height: {h}")

# Display the image with bounding boxes
cv2.imshow('Detected Objects', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
