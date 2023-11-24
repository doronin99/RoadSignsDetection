import os
import random
import json
import yaml
import shutil
from collections import defaultdict
from glob import glob


def create_yaml_from_class_map(class_map_path, yaml_output_path):
    """
    Creates a YAML file from a class_map.json file.
    :param class_map_path: path to the class_map.json file.
    :param yaml_output_path: path to the output YAML file.
    """
    with open(class_map_path, "r") as file:
        class_map = json.load(file)

    adjusted_class_map = {int(value - 1): key for key, value in class_map.items()}

    yaml_data = {
        "path": "./",
        "train": "train",
        "val": "valid",
        "names": adjusted_class_map,
    }

    with open(yaml_output_path, "w") as yaml_file:
        yaml.safe_dump(yaml_data, yaml_file, sort_keys=False)


def clean_data(annotation_folder, min_limit, max_limit):
    annotation_files = glob(os.path.join(annotation_folder, "*.txt"))

    class_counts = defaultdict(int)
    file_to_classes = defaultdict(set)

    for file in annotation_files:
        with open(file, "r") as f:
            lines = f.readlines()
        if lines:
            for line in lines:
                class_id = line.split()[0]
                file_to_classes[file].add(class_id)
                class_counts[class_id] += 1

    files_to_delete = set()
    for file, classes in file_to_classes.items():
        delete_file = any(
            class_counts[class_id] < min_limit for class_id in classes
        ) or any(class_counts[class_id] > max_limit for class_id in classes)
        if delete_file:
            files_to_delete.add(file)

    # Удаление файлов
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            jpg_file = file.replace(".txt", ".jpg")
            if os.path.exists(jpg_file):
                os.remove(jpg_file)


def reduce_background_images(annotation_folder, image_folder, keep_percentage=0.1):
    """
    reduces the number of background images to a percentage of the total number of images
    :param annotation_folder: path to the folder with annotations
    :param image_folder: path to the folder with images
    :param keep_percentage: proportion of background images to keep
    """
    background_files = []
    total_files = 0

    for filename in os.listdir(annotation_folder):
        if filename.endswith(".txt"):
            total_files += 1
            file_path = os.path.join(annotation_folder, filename)
            with open(file_path, "r") as file:
                if not file.read().strip():  # Файл пуст
                    background_files.append(filename)

    num_to_keep = int(total_files * keep_percentage)
    num_to_remove = len(background_files) - num_to_keep

    if num_to_remove > 0:
        files_to_remove = random.sample(background_files, num_to_remove)
        for filename in files_to_remove:
            os.remove(os.path.join(annotation_folder, filename))
            image_filename = filename.replace(".txt", ".jpg")
            os.remove(os.path.join(image_folder, image_filename))


def remove_small_classes(annotation_folder, min_objects):
    # Находим все файлы аннотаций
    annotation_files = glob(os.path.join(annotation_folder, "*.txt"))

    # Подсчет количества объектов для каждого класса
    class_counts = defaultdict(int)
    file_to_classes = defaultdict(set)

    for file in annotation_files:
        with open(file, "r") as f:
            lines = f.readlines()
        for line in lines:
            class_id = line.split()[0]
            file_to_classes[file].add(class_id)
            class_counts[class_id] += 1

    for file, classes in file_to_classes.items():
        if any(class_counts[class_id] < min_objects for class_id in classes):
            os.remove(file)
            image_file = file.replace(".txt", ".jpg")
            if os.path.exists(image_file):
                os.remove(image_file)


def split_data(source_folder, train_folder, valid_folder, seed=42, train_size=0.8):
    """
    Разбивает данные на тренировочную и валидационную выборки.
    :param source_folder: Source folder with images and annotations
    :param train_folder: train folder
    :param valid_folder: valid folder
    :param train_size: train size in percent
    :param seed: random seed
    """
    random.seed(seed)
    files = [file for file in os.listdir(source_folder) if file.endswith(".jpg")]
    random.shuffle(files)

    train_count = int(len(files) * train_size)
    train_files = files[:train_count]
    valid_files = files[train_count:]

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(valid_folder, exist_ok=True)

    for file in train_files:
        shutil.copy(os.path.join(source_folder, file), os.path.join(train_folder, file))
        shutil.copy(
            os.path.join(source_folder, file.replace(".jpg", ".txt")),
            os.path.join(train_folder, file.replace(".jpg", ".txt")),
        )

    for file in valid_files:
        shutil.copy(os.path.join(source_folder, file), os.path.join(valid_folder, file))
        shutil.copy(
            os.path.join(source_folder, file.replace(".jpg", ".txt")),
            os.path.join(valid_folder, file.replace(".jpg", ".txt")),
        )


def remove_classes_from_yaml(yaml_path, top_classes):
    """
    Deletes classes from a YAML file.
    """
    with open(yaml_path, "r") as file:
        data = yaml.safe_load(file)

    if "names" in data and isinstance(data["names"], dict):
        index_to_name = data["names"]

        updated_classes = {}
        for new_index, old_index in enumerate(top_classes):
            if old_index in index_to_name:
                updated_classes[new_index] = index_to_name[old_index]
            else:
                print(f"Class index {old_index} not found in YAML 'names'")

        sorted_classes = {str(k): v for k, v in sorted(updated_classes.items())}
        data["names"] = sorted_classes
    else:
        raise ValueError(
            "YAML file format is not as expected. 'names' should be a dictionary."
        )

    with open(yaml_path, "w") as file:
        yaml.safe_dump(data, file, sort_keys=False)


import os


def filter_annotations(annotation_folder, top_classes, threshold):
    class_mapping = {old: new for new, old in enumerate(top_classes)}
    class_counts = {class_id: 0 for class_id in top_classes}

    for filename in os.listdir(annotation_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(annotation_folder, filename)
            with open(file_path, "r") as file:
                lines = file.readlines()

            updated_lines = []
            for line in lines:
                parts = line.split()
                class_index = int(parts[0])
                if (
                    class_index in class_mapping
                    and class_counts[class_index] < threshold
                ):
                    class_counts[class_index] += 1
                    parts[0] = str(class_mapping[class_index])
                    updated_lines.append(" ".join(parts) + "\n")

            if updated_lines:
                with open(file_path, "w") as file:
                    file.writelines(updated_lines)
            else:
                os.remove(file_path)
                jpg_file_path = os.path.splitext(file_path)[0] + ".jpg"
                if os.path.exists(jpg_file_path):
                    os.remove(jpg_file_path)

    return class_mapping


def update_yaml_classes(yaml_path, class_mapping):
    with open(yaml_path, "r") as file:
        yaml_data = yaml.safe_load(file)

    if "names" in yaml_data:
        updated_classes = {}
        for old_index, new_index in class_mapping.items():
            if old_index in yaml_data["names"]:
                updated_classes[new_index] = yaml_data["names"][old_index]

        yaml_data["names"] = updated_classes

    with open(yaml_path, "w") as file:
        yaml.safe_dump(yaml_data, file, sort_keys=False)
