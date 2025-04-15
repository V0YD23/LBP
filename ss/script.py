import cv2
import numpy as np
import pandas as pd

# Load the image
img = cv2.imread('structure.png')

# Crop to the grid area if needed
# img = img[y1:y2, x1:x2]

# Resize to 21x21 if needed
img_resized = cv2.resize(img, (21, 21), interpolation=cv2.INTER_NEAREST)

# Define color to angle mapping (BGR format)
color_map = {
    (0, 0, 0): 0,         # Black
    (0, 0, 255): 50,      # Red
    (0, 255, 255): 100,   # Yellow
    # Add more mappings as needed
}

# Function to find closest color
def closest_color(bgr):
    min_dist = float('inf')
    angle = -1
    for color, ang in color_map.items():
        dist = np.linalg.norm(np.array(bgr) - np.array(color))
        if dist < min_dist:
            min_dist = dist
            angle = ang
    return angle

# Create the angle matrix
angle_matrix = []
for row in img_resized:
    angle_row = []
    for pixel in row:
        angle_row.append(closest_color(pixel))
    angle_matrix.append(angle_row)

# Save to Excel
df = pd.DataFrame(angle_matrix)
df.to_excel('phase_angles.xlsx', index=False, header=False)
