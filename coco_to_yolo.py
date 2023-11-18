import json
import os

image_folder = 'rtsd-frames3'# replace with your image folder
anno = 'train_anno.json' # replace with your annotation file

with open(anono) as f:
    coco_annotations = json.load(f)

category_id_to_index = {category['id']: i for i, category in enumerate(coco_annotations['categories'])}

def convert_to_yolo_format(box, img_width, img_height):
    '''
    convert COCO format to YOLO format
    @param box: COCO format bounding box
    @param img_width: image width
    @param img_height: image height
    '''
    x_center = (box[0] + box[2] / 2) / img_width
    y_center = (box[1] + box[3] / 2) / img_height
    width = box[2] / img_width
    height = box[3] / img_height
    return x_center, y_center, width, height

def create_empty_annotations(image_folder):
    """
    Создает пустые .txt файлы для изображений без детектируемых объектов.
    :param image_folder: Путь к папке с изображениями.
    """

    image_files = [file for file in os.listdir(image_folder) if file.endswith('.jpg')]

    for image_file in image_files:
        annotation_file = os.path.join(image_folder, image_file.replace('.jpg', '.txt'))

        if not os.path.exists(annotation_file):
            open(annotation_file, 'w').close()
            print(f"Created empty annotation for {image_file}")

for img in coco_annotations['images']:
    img_width, img_height = img['width'], img['height']
    annotations = [a for a in coco_annotations['annotations'] if a['image_id'] == img['id']]
    
    with open(f'{img["file_name"].replace(".jpg", ".txt")}', 'w') as f:
        for annotation in annotations:
            category_index = category_id_to_index[annotation['category_id']]
            yolo_box = convert_to_yolo_format(annotation['bbox'], img_width, img_height)
            f.write(f"{category_index} {' '.join(map(str, yolo_box))}\n")

create_empty_annotations(image_folder)