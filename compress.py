import cv2
import os
from PIL import Image

# === CONFIG ===
input_path = 'convolution-animation.mp4'
output_path = 'compressed_output.mp4'
target_size_mb = 50
frame_skip = 2  # Speeds up 2x
resize_factor = 0.5  # Scale to 50% size
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec

# === Step 1: Read input video ===
cap = cv2.VideoCapture(input_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * resize_factor)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * resize_factor)

frames = []
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % frame_skip == 0:
        frame = cv2.resize(frame, (width, height))
        frames.append(frame)
    frame_count += 1

cap.release()

# === Step 2: Estimate optimal FPS for compression ===
# Rough calculation: uncompressed size (bytes) ≈ width * height * 3 (RGB) * frames
raw_bytes = width * height * 3 * len(frames)
raw_mb = raw_bytes / (1024 * 1024)

scaling_factor = target_size_mb / raw_mb
compressed_fps = max(5, int(fps * scaling_factor))  # Avoid too low FPS

print(f"Original frames: {frame_count}, Used: {len(frames)}")
print(f"Estimated size before compression: {raw_mb:.2f} MB")
print(f"Adjusted output FPS: {compressed_fps}")

# === Step 3: Write compressed video ===
out = cv2.VideoWriter(output_path, fourcc, 60, (width, height))
for frame in frames:
    out.write(frame)
out.release()

# # === Step 4 (optional): Convert to GIF ===
# gif_frames = [cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames]
# pil_frames = [Image.fromarray(f) for f in gif_frames]
# pil_frames[0].save(
#     "output.gif",
#     save_all=True,
#     append_images=pil_frames[1:],
#     duration=int(1000 / compressed_fps),
#     loop=0
# )

# === Final size check ===
final_size = os.path.getsize(output_path) / (1024 * 1024)
print(f"\n✅ Final video size: {final_size:.2f} MB")
