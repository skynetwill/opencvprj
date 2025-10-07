import cv2
import numpy as np

# Load the source image
image = cv2.imread('exchange_station.PNG')
if image is None:
    print("Error: Could not load image.")
    exit()

# --- Step 1: Color Segmentation in HSV Space ---
# Convert the BGR image to the HSV (Hue, Saturation, Value) color space.
# This space is much better for isolating colors than BGR or grayscale.
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the range for the bright blue/cyan color of the lights in HSV.
# These values are tuned to select the specific color of the lights.
lower_blue = np.array([85, 100, 100])
upper_blue = np.array([110, 255, 255])

# Create a binary mask where white pixels represent the colors in our defined range.
color_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

# --- Step 2: Refine the Mask ---
# Use morphological operations to clean up the mask.
# Dilation helps to fill in small gaps within the detected light bars,
# creating more solid and complete shapes.
kernel = np.ones((5, 5), np.uint8)
dilated_mask = cv2.dilate(color_mask, kernel, iterations=1)

# --- Step 3: Find and Filter Contours ---
# Find contours on the cleaned, color-segmented mask.
contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a copy of the original image to draw the results on.
output_image = image.copy()

# Iterate through each found contour.
for contour in contours:
    # Filter 1: Area - discard contours that are too small to be the lights.
    area = cv2.contourArea(contour)
    if area > 100:  # This threshold may need minor tuning.

        # Filter 2: Shape (Polygon Approximation)
        perimeter = cv2.arcLength(contour, True)
        epsilon = 0.03 * cv2.arcLength(contour, True)  # More tolerance
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # The arrow shape is well approximated by 6 to 8 vertices.
        if 6 <= len(approx) <= 8:

            # Filter 3: Aspect Ratio - ensure the shape is not too long or too tall.
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.7 < aspect_ratio < 1.4:
                # If all filters pass, draw the bounding box.
                cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(output_image, f"v:{len(approx)}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# --- Step 4: Display Results ---
# Display the intermediate steps for debugging and understanding.
cv2.imshow('Original Image', image)
cv2.imshow('Color Mask', color_mask)
cv2.imshow('Final Detection', output_image)

# Save the final result
cv2.imwrite("detection_result_final.png", output_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
