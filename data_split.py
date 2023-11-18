import os
import random
import shutil

def split_data(source_folder, train_folder, valid_folder,seed=42, train_size=0.8):
    """
    Splits source_folder on train and valid
    :param source_folder: Source folder with images and annotations
    :param train_folder: train folder
    :param valid_folder: valid folder
    :param train_size: train size in percent
    :param seed: random seed
    """
    random.seed(seed)
    files = [file for file in os.listdir(source_folder) if file.endswith('.jpg')]
    random.shuffle(files)

    train_count = int(len(files) * train_size)
    train_files = files[:train_count]
    valid_files = files[train_count:]

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(valid_folder, exist_ok=True)

    for file in train_files:
        shutil.copy(os.path.join(source_folder, file), os.path.join(train_folder, file))
        shutil.copy(os.path.join(source_folder, file.replace('.jpg', '.txt')), os.path.join(train_folder, file.replace('.jpg', '.txt')))

    for file in valid_files:
        shutil.copy(os.path.join(source_folder, file), os.path.join(valid_folder, file))
        shutil.copy(os.path.join(source_folder, file.replace('.jpg', '.txt')), os.path.join(valid_folder, file.replace('.jpg', '.txt')))

split_data('rtsd-frames3', 'datasets/train_40cls', 'datasets/valid_40cls', random=42, train_size=0.8)
