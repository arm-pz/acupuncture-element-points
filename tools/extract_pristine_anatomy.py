from PIL import Image
import numpy as np

src_path = r'C:/Users/abdul/.gemini/antigravity/brain/8aabb083-e170-4acf-84b2-0047221a9782/.user_uploaded/media_1794324661411_7a582507.png'
im = Image.open(src_path).convert('RGB')
arr = np.array(im)
H, W, _ = arr.shape
r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

# Output image: 255 is white
out = np.ones((H, W), dtype=np.uint8) * 255

# 1. Identify non-body regions to wipe completely:
# - Copyright area (bottom left)
# - Perineum insets (top right, bottom right)
# - Left margin labels: x < 78 for y > 320
# - Right margin labels: x > 235 for y > 180 (except the right arm which is x in [240, 275] for y < 350)
# Let's inspect where the right arm is:
# Right shoulder / arm: y in [180, 400], x up to 275.
# Above y=180: head is x in [90, 210]. Inset is x > 215.

# Let's check color for ink:
# Dark pixels (r<130, g<130, b<130) that are NOT blue and NOT orange
is_blue = (b > 100) & (b > r + 25)
is_orange = (r > 150) & (r > b + 40)
gray = 0.299 * r + 0.587 * g + 0.114 * b
is_dark = (gray < 160) & ~is_blue & ~is_orange

# Coordinate exclusion masks:
exclude = np.zeros((H, W), dtype=bool)
# Top-right inset
exclude[:140, 215:] = True
# Bottom-right inset
exclude[510:, 195:] = True
# Copyright bottom-left
exclude[565:, :195] = True
# Labels on left of abdomen: x < 76 below y=330
exclude[330:530, :76] = True
# Labels and ruler on right of chest:
# Sternal angle numbers '1.6', '4' etc. outside the arm/chest
# The chest right border is at x ≈ 235-245.
# Ruler lines outside the body: x in [245, 275] for y in [210, 310] has ruler line.
# Dashed horizontal leader lines:
# They occur at specific y levels where points are located, e.g. y around 146, 170, 213, 225, 236, 253, 266, 282, 300, 328, 344, 362, 380, 447, 456, 465, 481, 494, 510
# For each of these horizontal dashed lines, they extend from x=155 to x=280 or x=70 to x=145.

# Let's clean row by row:
for y in range(H):
    for x in range(W):
        if is_dark[y, x] and not exclude[y, x]:
            out[y, x] = int(gray[y, x])

# Remove horizontal dashed leader lines:
# A dashed leader line has consecutive short segments of 2-4 dark pixels followed by white gaps, on a single row!
# Whereas ribs and contours have continuous lines across multiple rows and columns.
for y in range(140, 530):
    # Check if this row has horizontal dashes
    row = (out[y, :] < 200).astype(int)
    # Check on right side x from 155 to 290:
    right_seg = row[155:290]
    # If it has many transitions (on/off/on/off) in a single row without vertical support:
    diffs = np.sum(np.abs(np.diff(right_seg)))
    if diffs >= 6: # characteristic of dashed line
        # Check if adjacent rows (y-1, y+1) are mostly white in this segment:
        above = np.sum(out[y-1, 155:290] < 200)
        below = np.sum(out[y+1, 155:290] < 200)
        if above < 15 and below < 15:
            # It's an isolated horizontal dashed line! Remove it.
            out[y, 155:290] = 255

    # Check on left side x from 70 to 145:
    left_seg = row[70:145]
    diffs_l = np.sum(np.abs(np.diff(left_seg)))
    # But be careful not to remove ribs! Ribs are curved and exist across multiple rows.
    if diffs_l >= 6:
        above_l = np.sum(out[y-1, 70:145] < 200)
        below_l = np.sum(out[y+1, 70:145] < 200)
        # Only remove if isolated single row dashed line
        if above_l < 10 and below_l < 10 and y > 380: # below the rib cage
            out[y, 70:145] = 255

# Reconnect the vertical midline line at x=150
for y in range(145, 515):
    for x in range(149, 152):
        if out[y, x] > 180:
            out[y, x] = 30

clean_img = Image.fromarray(out)
clean_img.save("tools/torso_pristine_anatomy.png")
print("Saved tools/torso_pristine_anatomy.png successfully!")
