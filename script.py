import numpy as np
import matplotlib.pyplot as plt

# Define parameters
size = 30  # 30x30 elements
wavelength = 2.1  # Half-wavelength periodicity
k = 2 * np.pi / wavelength  # Wave number
# P = wavelength/2
P = 0.993
source_x, source_y, z_feed = 15, 15, 30*0.8  # Feed at (15,15,50)
psi_0 = 0  # Phase offset

# Grid setup
x_vals = np.linspace(0, size - 1, size)
y_vals = np.linspace(0, size - 1, size)
psi_matrix = np.zeros((size, size))  # Store computed phases

# Compute phase distribution
for i, x in enumerate(x_vals):
    for j, y in enumerate(y_vals):
        R_i = np.sqrt((x - source_x)**2 + (y - source_y)**2 + z_feed**2)  # Distance to feed
        psi_matrix[j, i] = k * (R_i - z_feed) + psi_0

# Normalize phase values to [0, 360] degrees
psi_matrix = np.mod(np.degrees(psi_matrix), 360)

# Create plot
plt.figure(figsize=(8, 6))
plt.imshow(psi_matrix, cmap="hot", origin="lower", extent=[0, size, 0, size], vmin=0, vmax=360)
plt.colorbar(label="Phase (degrees)")

# Overlay circular aperture boundary
R_aperture = (size / 2 + 0.1)*P  # Adjusted margin
circle = plt.Circle((source_x, source_y), R_aperture, color="blue", fill=False, linewidth=1.5)
plt.gca().add_patch(circle)

# Labels and formatting
plt.xlabel("Elements in x-direction")
plt.ylabel("Elements in y-direction")
plt.title("Phase Distribution of Circular Aperture Transmitarray")
plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)

# Save and show
plt.savefig("phase_distribution_hot.png", dpi=300)
# plt.show()
