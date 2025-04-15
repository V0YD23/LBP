import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# Parameters
num_blocks = 29
physical_size = 101.5  # mm
element_spacing = physical_size / num_blocks  # ~3.5 mm per element

wavelength = 12.43  # mm
k = 2 * np.pi / wavelength  # Wave number
P = wavelength / 2

# Feed location (center of the grid)
source_x, source_y = physical_size / 2, physical_size / 2
z_feed = physical_size*0.5  # mm (height)
psi_0 = 0

# Grid setup (physical coordinates)
x_vals = np.linspace(0, physical_size - element_spacing, num_blocks)
y_vals = np.linspace(0, physical_size - element_spacing, num_blocks)
psi_matrix = np.zeros((num_blocks, num_blocks))

# Compute phase distribution
for i, x in enumerate(x_vals):
    for j, y in enumerate(y_vals):
        R_i = np.sqrt((x - source_x)**2 + (y - source_y)**2 + z_feed**2)
        psi_matrix[j, i] = k * (R_i - z_feed) + psi_0

# Normalize phase to [0, 360]
psi_matrix = np.mod(np.degrees(psi_matrix), 360)

# Plotting
plt.figure(figsize=(8, 6))
plt.imshow(
    psi_matrix, cmap="hot", origin="lower",
    extent=[0, physical_size, 0, physical_size],
    vmin=0, vmax=360
)
plt.colorbar(label="Phase (degrees)")

# Overlay circular aperture boundary
R_aperture = (physical_size / 2 + 0.1) * P / element_spacing  # radius in grid units
circle = plt.Circle((source_x, source_y), R_aperture, color="blue", fill=False, linewidth=1.5)
plt.gca().add_patch(circle)

# Labels and formatting
plt.xlabel("x position (mm)")
plt.ylabel("y position (mm)")
plt.title("Phase Distribution of Circular Aperture Transmitarray")
plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)

# Save and show
plt.savefig("phase_distribution_hot.png", dpi=300)
# plt.show()

# Save psi_matrix (phase angles) to Excel
df = pd.DataFrame(psi_matrix)
df.to_excel("phase_distribution_angles.xlsx", index=False, header=False)
