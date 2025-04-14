import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
from PIL import Image

input_img = Image.open('assets/snake.jpeg').convert("RGB").resize((128, 128))

input_image = np.array(input_img, dtype=np.float32)

# Kernel has 3 layers for each channel 
kernel = np.array([[
   [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
], [
   [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
], [
   [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],  
]], dtype=np.float32) 


pad = kernel.shape[0] // 2
padded_input = np.pad(input_image, ((pad, pad), (pad, pad), (0, 0)), mode='constant')
output = np.zeros_like(input_image)

# Create a list of all valid (i, j) positions (for each pixel in the image)
positions = [(i, j) for i in range(output.shape[0]) for j in range(output.shape[1])]


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

def update(frame):
    global output
    i, j = positions[frame]
    i_pad, j_pad = i + pad, j + pad
    
    # Apply convolution on each RGB channel separately
    for c in range(3):  
        region = padded_input[i_pad - 1:i_pad + 2, j_pad - 1:j_pad + 2, c]
        conv_value = np.sum(region * kernel[c])
        output[i, j, c] = conv_value  # Store raw float value for each channel

    display_output = np.clip(output, 0, 255).astype(np.uint8)
    
    im2.set_data(display_output)
    rect.set_xy((j_pad - 3, i_pad - 3))
    return [im1, im2, rect]

ani = FuncAnimation(fig, update, frames=len(positions), interval=1, blit=True)
plt.tight_layout()
plt.show()
