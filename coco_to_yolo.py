import json
import os


def read_coco_annotations(annotation_file):
    """
    Читает аннотации в формате COCO из файла.
    :param annotation_file: Путь к файлу аннотации.
    :return: Словарь аннотаций COCO.
    """
    with open(annotation_file) as f:
        return json.load(f)


def convert_to_yolo_format(box, img_width, img_height):
    """
    Конвертирует формат ограничивающего прямоугольника COCO в формат YOLO.
    """
    x_center = (box[0] + box[2] / 2) / img_width
    y_center = (box[1] + box[3] / 2) / img_height
    width = box[2] / img_width
    height = box[3] / img_height
    return x_center, y_center, width, height


def convert_annotations_to_yolo(image_folder, coco_annotations):
    """
    Конвертирует аннотации из формата COCO в формат YOLO и записывает их в соответствующие файлы.
    """
    category_id_to_index = {
        category["id"]: i for i, category in enumerate(coco_annotations["categories"])
    }

    for img in coco_annotations["images"]:
        img_width, img_height = img["width"], img["height"]
        annotations = [
            a for a in coco_annotations["annotations"] if a["image_id"] == img["id"]
        ]

        with open(
            os.path.join(image_folder, img["file_name"].replace(".jpg", ".txt")), "w"
        ) as f:
            for annotation in annotations:
                category_index = category_id_to_index[annotation["category_id"]]
                yolo_box = convert_to_yolo_format(
                    annotation["bbox"], img_width, img_height
                )
                f.write(f"{category_index} {' '.join(map(str, yolo_box))}\n")


def create_empty_annotations(image_folder):
    """
    Создает пустые .txt файлы для изображений без детектируемых объектов.
    """
    image_files = [file for file in os.listdir(image_folder) if file.endswith(".jpg")]

    for image_file in image_files:
        annotation_file = os.path.join(image_folder, image_file.replace(".jpg", ".txt"))

        if not os.path.exists(annotation_file):
            open(annotation_file, "w").close()
            print(f"Created empty annotation for {image_file}")
