# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
import matplotlib
# from PIL import Image

# matplotlib.use("Agg")
# input_img1 = Image.open('ILSVRC2012_val_00005027.jpeg').convert("L").resize((256, 256))
# input_img2 = Image.open('ILSVRC2012_val_00005050.jpeg').convert("L").resize((256, 256))

# input_image = np.array(input_img2, dtype=np.float32)

# kernel = np.array([
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, 8, 8, -1, -1],
#     [-1, -1, 8, 8, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1]
# ], dtype=np.float32)

# # 3. Padding the input
# pad = kernel.shape[0] // 2
# padded_input = np.pad(input_image, pad, mode='constant')
# output = np.zeros_like(input_image)

# # 4. Create a list of all valid (i, j) positions
# positions = [(i, j) for i in range(output.shape[0]) for j in range(output.shape[1])]

# # 5. Setup the figure and axes
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
# im1 = ax1.imshow(padded_input, cmap='gray')
# rect = plt.Rectangle((0, 0), 6, 6, edgecolor='red', facecolor='none', lw=2)
# ax1.add_patch(rect)
# ax1.set_title("Sliding Kernel")
# ax1.axis('off')

# im2 = ax2.imshow(output, cmap='grey', vmin = 0, vmax = 255)
# ax2.set_title("Output Image")
# ax2.axis('off')

# def normalize_to_uint8(arr):
#     arr_min = arr.min()
#     arr_max = arr.max()
#     if arr_max == arr_min:
#         return np.zeros_like(arr, dtype=np.uint8)
#     norm = (arr - arr_min) / (arr_max - arr_min)  # scale to 0–1
#     return (norm * 255).astype(np.uint8)

# def update(frame):
#     global output
#     i, j = positions[frame]
#     i_pad, j_pad = i + pad, j + pad
#     region = padded_input[i_pad - 3:i_pad + 3, j_pad - 3:j_pad + 3]
#     conv_value = np.sum(region * kernel)
#     output[i, j] = conv_value  # Store raw float value

#     # Only normalize for display, not in-place
#     display_output = normalize_to_uint8(output)

#     im2.set_data(display_output)
#     rect.set_xy((j_pad - 3, i_pad - 3))
#     return [im1, im2, rect]


# # 7. Animate it
# ani = FuncAnimation(fig, update, frames=len(positions), interval=1, blit=True)
# ani.save('animation.gif', writer='pillow', fps=60)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
from PIL import Image

# matplotlib.use("Agg")

# Load and resize the image to 256x256 (RGB image)
input_img = Image.open('ILSVRC2012_val_00005050.jpeg').convert("RGB").resize((128, 128))

# Convert the image into a NumPy array (shape: 256x256x3)
input_image = np.array(input_img, dtype=np.float32)


# Define the kernel (same kernel for all three channels)
kernel = np.array([[
   [-1, -1, -1],
    [-1, 9, -1],
    [-1, -1, -1],
], [
    [0, 0, 0],
    [0, 1/2, 0],
    [0, 0, 0],
], [
   [-1, -1, -1],
    [-1, 9, -1],
    [-1, -1, -1],  
]], dtype=np.float32) 

# Padding the input (same for all channels)
pad = kernel.shape[0] // 2
padded_input = np.pad(input_image, ((pad, pad), (pad, pad), (0, 0)), mode='constant')

# Prepare output container (same size as the input)
output = np.zeros_like(input_image)

# Create a list of all valid (i, j) positions (for each pixel in the image)
positions = [(i, j) for i in range(output.shape[0]) for j in range(output.shape[1])]

# Setup the figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
print(input_image)
im1 = ax1.imshow(input_image.astype(np.uint8))  # Initial input image
rect = plt.Rectangle((0, 0), 6, 6, edgecolor='red', facecolor='none', lw=2)
ax1.add_patch(rect)
ax1.set_title("Sliding Kernel")
ax1.axis('off')

im2 = ax2.imshow(output.astype(np.uint8))  # Output image
ax2.set_title("Output Image")
ax2.axis('off')

# Normalize to uint8 for display
def normalize_to_uint8(arr):
    arr_min = arr.min()
    arr_max = arr.max()
    if arr_max == arr_min:
        return np.zeros_like(arr, dtype=np.uint8)
    norm = (arr - arr_min) / (arr_max - arr_min)  # scale to 0–1
    return (norm * 255).astype(np.uint8)

# Update function for animation
def update(frame):
    global output
    i, j = positions[frame]
    i_pad, j_pad = i + pad, j + pad
    
    # Apply convolution on each RGB channel separately
    for c in range(3):  # Iterate over R, G, and B channels
        region = padded_input[i_pad - 1:i_pad + 2, j_pad - 1:j_pad + 2, c]
        conv_value = np.sum(region * kernel[c])
        output[i, j, c] = conv_value  # Store raw float value for each channel

    # Normalize and update the output image for display
    display_output = np.clip(output, 0, 255).astype(np.uint8)
    
    # Update images
    im2.set_data(display_output)
    rect.set_xy((j_pad - 3, i_pad - 3))
    return [im1, im2, rect]

# Animate it
ani = FuncAnimation(fig, update, frames=len(positions), interval=1, blit=True)
plt.tight_layout()
plt.show()
