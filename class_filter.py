import os
import pandas as pd
import yaml

yaml_path = 'trafic_sign_40.yaml' #replace with your path to YAML file
annotation_folder = 'rtsd-frames3' #replace with your path to annotation folder

def get_top_classes(annotation_folder, top_n=40):
    """
    return list of top_n classes by frequency.
    """
    class_list = []
    for filename in os.listdir(annotation_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(annotation_folder, filename)
            with open(file_path, 'r') as file:
                annotations = file.readlines()
                for annotation in annotations:
                    class_index = int(annotation.split()[0])
                    class_list.append(class_index)

    class_series = pd.Series(class_list)
    top_classes = class_series.value_counts().head(top_n).index.tolist()
    return top_classes

def filter_annotations(annotation_folder, top_classes):
    """
    filters annotations, leaving only lines with classes from top_classes.
    """
    class_mapping = {old: new for new, old in enumerate(top_classes)}

    for filename in os.listdir(annotation_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(annotation_folder, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()

            updated_lines = []
            for line in lines:
                parts = line.split()
                class_index = int(parts[0])
                if class_index in class_mapping:
                    parts[0] = str(class_mapping[class_index])
                    updated_lines.append(' '.join(parts) + '\n')

            with open(file_path, 'w') as file:
                file.writelines(updated_lines)

def remove_classes_from_yaml(yaml_path, top_classes):
    """
    removes classes from yaml file
    """
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)

    if 'names' in data and isinstance(data['names'], dict):
        index_to_name = data['names']

        updated_classes = {}
        for new_index, old_index in enumerate(top_classes):
            if old_index in index_to_name:
                updated_classes[new_index] = index_to_name[old_index]
            else:
                print(f"Class index {old_index} not found in YAML 'names'")

        sorted_classes = {str(k): v for k, v in sorted(updated_classes.items())}
        data['names'] = sorted_classes
    else:
        raise ValueError("YAML file format is not as expected. 'names' should be a dictionary.")

    with open(yaml_path, 'w') as file:
        yaml.safe_dump(data, file, sort_keys=False)

top_classes = get_top_classes(annotation_folder)
filter_annotations(annotation_folder,top_classes)
remove_classes_from_yaml(yaml_path, top_classes)
