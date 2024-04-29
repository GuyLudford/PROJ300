import cv2
import numpy as np

# Load your image
image = cv2.imread("Blank Wall.jpg")

# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Split channels
H, S, V = cv2.split(hsv)

# Apply Canny edge detection to each channel
edges_H = cv2.Canny(H, 50, 200)
edges_S = cv2.Canny(S, 50, 200)
edges_V = cv2.Canny(V, 50, 200)

# Combine the edges
combined_edges = edges_H | edges_S | edges_V

# Find contours
contours, _ = cv2.findContours(combined_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw rectangles around detected regions
for cnt in contours:
    if cv2.contourArea(cnt) > 1000:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the final output
cv2.imshow("Color Contrasting Regions", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
