import cv2
import numpy as np

# Load the image
image = cv2.imread('Blank Wall.jpg', cv2.IMREAD_GRAYSCALE)

# Apply Harris corner detection
corners = cv2.cornerHarris(image, blockSize=2, ksize=3, k=0.04)

# Threshold the corner response
threshold = 0.0001 * corners.max()
corner_image = np.zeros_like(image)
corner_image[corners > threshold] = 255

# Display the result
cv2.imshow('Climbing Holds', corner_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
