import cv2
import numpy as np

# Assume 'image' is your source image and 'binary_image' is the thresholded/binary version.
# For demonstration, let's create placeholders.
image = cv2.imread('exchange_station.PNG')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

cv2.imshow('image', image)
cv2.imshow('gray', gray_image)
cv2.imshow('binary', binary_image)


# 1. Find all contours from the binary image, as described in the document. [cite: 13]
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# cv2.imshow('contours', contours)
# Create a copy of the original image to draw the results on.
output_image = image.copy()

# 2. Iterate through each found contour.
for contour in contours:
    # --- Improvement 1: Filter by Area ---
    # Calculate the area of the contour.
    # This is a very effective way to remove small, irrelevant noise.
    # The area values (e.g., > 100) will need tuning based on the image resolution.
    area = cv2.contourArea(contour)
    if area > 600:  # Only consider contours with a significant area.

        # --- Use the same polygon approximation logic from the document. ---
        # Calculate the perimeter.
        perimeter = cv2.arcLength(contour, True)
        # Approximate the contour to a polygon. [cite: 23]
        epsilon = 0.02 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # --- Improvement 2: Relax the Shape (Vertex Count) Filter ---
        # The arrow shape is like a hexagon, but may be detected with 5 to 8 vertices.
        # By checking a range, we make the detection more robust.
        if 5 <= len(approx) <= 6:
            # --- Draw the final bounding box as before. ---
            # Calculate a simple bounding rectangle for the filtered contour. [cite: 16]
            x, y, w, h = cv2.boundingRect(contour)

            # Draw the red rectangle on the output image. [cite: 16]
            cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Display the final result.
cv2.imshow('Improved Detection', output_image)
cv2.imwrite("detection_result_2.png", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()