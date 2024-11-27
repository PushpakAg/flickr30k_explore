import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

images_dir = "flickr30k/Images/"
annotations_dir = "Annotations/"
captions_dir = "Sentences/"

image_id = "10002456"
image_path = os.path.join(images_dir, f"{image_id}.jpg")
annotation_path = os.path.join(annotations_dir, f"{image_id}.xml")
caption_path = os.path.join(captions_dir, f"{image_id}.txt")

image = Image.open(image_path)

tree = ET.parse(annotation_path)
root = tree.getroot()

entity_colors = [
    (1.0, 0.0, 0.0),   # Red
    (0.0, 1.0, 0.0),   # Green
    (0.0, 0.0, 1.0),   # Blue
    (1.0, 0.5, 0.0),   # Orange
    (0.6, 0.0, 0.6),   # Purple
    (0.0, 1.0, 1.0),   # Cyan
    (1.0, 0.0, 1.0),   # Magenta
    (1.0, 1.0, 0.0),   # Yellow
    (0.5, 1.0, 0.0),   # Lime
    (0.0, 0.5, 0.5)    # Teal
]

bboxes = []
for obj in root.findall('.//object'):
    names = [name.text for name in obj.findall('name')]
    bbox = obj.find('.//bndbox')
    if bbox is not None:
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        bboxes.append({'names': names, 'bbox': (xmin, ymin, xmax, ymax)})

fig, ax = plt.subplots()
ax.imshow(image)

for item in bboxes:
    (xmin, ymin, xmax, ymax) = item['bbox']
    color_index = int(item['names'][0]) % len(entity_colors)
    color = entity_colors[color_index]
    rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                             linewidth=2, edgecolor=color, facecolor=color, alpha=0.3)
    ax.add_patch(rect)
    ax.text(xmin, ymin, ', '.join(item['names']), color=color, bbox=dict(facecolor=color, alpha=0.5))

plt.axis("off")
plt.show()

if os.path.exists(caption_path):
    with open(caption_path, 'r') as file:
        captions = file.readlines()

    print("\nCaptions:")
    for caption in captions:
        styled_caption = caption.strip()
        for i, color in enumerate(entity_colors):
            entity_tag = f'/EN#{i+1}/'
            if entity_tag in styled_caption:
                color_code = f"\033[38;2;{int(color[0]*255)};{int(color[1]*255)};{int(color[2]*255)}m"
                styled_caption = styled_caption.replace(entity_tag, color_code + entity_tag)
                styled_caption = styled_caption.replace(']', ']\033[0m')
        print(styled_caption)
else:
    print("No captions found.")