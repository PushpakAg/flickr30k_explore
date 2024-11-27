import os
import random
import xml.etree.ElementTree as ET

annotations_dir = "Annotations/"

if not os.path.exists(annotations_dir) or not os.listdir(annotations_dir):
    print(f"The directory '{annotations_dir}' does not exist or is empty.")
else:
    xml_files = [f for f in os.listdir(annotations_dir) if f.endswith('.xml')]
    random_file = random.choice(xml_files)
    annotation_path = os.path.join(annotations_dir, random_file)

    with open(annotation_path, 'r') as file:
        xml_content = file.read()

    root = ET.fromstring(xml_content)

    bboxes = []
    scene_nobndbox_flags = []

    for obj in root.findall('.//object'):
        names = [name.text for name in obj.findall('name')]

        bbox = obj.find('.//bndbox')
        if bbox is not None:
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            bboxes.append({'names': names, 'bbox': (xmin, ymin, xmax, ymax)})

        scene = obj.find('.//scene')
        nobndbox = obj.find('.//nobndbox')
        if scene is not None or nobndbox is not None:
            scene_nobndbox_flags.append({
                'names': names,
                'scene': scene.text if scene is not None else None,
                'nobndbox': nobndbox.text if nobndbox is not None else None
            })

    print(f"Processing file: {random_file}")

    print("\nBounding boxes with object names:")
    for item in bboxes:
        print(f"Names: {item['names']}, Bounding box: {item['bbox']}")
        
    print("\nScene and no bounding box flags with object names:")
    for item in scene_nobndbox_flags:
        print(f"Names: {item['names']}, Scene: {item['scene']}, NoBndBox: {item['nobndbox']}")
