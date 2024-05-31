import json
import os
import re

# Pfad zum Ordner mit den JSON-Dateien
json_folder = "C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/json_test"

# Funktion zur Konvertierung der Koordinaten in das YOLO-Format
def convert_coordinates(width, height, bbox):
    x_center = bbox['left'] + bbox['width'] / 2
    y_center = bbox['top'] + bbox['height'] / 2
    x_center /= width
    y_center /= height
    bbox_width = bbox['width'] / width
    bbox_height = bbox['height'] / height
    return x_center, y_center, bbox_width, bbox_height

# Funktion zur Erstellung des YOLO-Labels für eine JSON-Datei
def create_yolo_labels(json_file):
    with open(os.path.join(json_folder, json_file), 'r') as file:
        data = json.load(file)

    # Extrahiere Metadaten
    height = data['media_attributes']['height']
    width = data['media_attributes']['width']
    # Extrahiere den Basename der JSON-Datei (ohne Pfad und Erweiterung)
    base_filename = os.path.splitext(json_file)[0]
    print(base_filename)
    # Entferne das Suffix '_combined_###_####.mp4' aus dem Basename
    base_filename_cleaned = re.sub(r'_combined_\d+_\d+\.mp4', '', base_filename)
    print(base_filename_cleaned)

    # Erstelle einen Ordner für die Frames dieser JSON-Datei
    output_folder = os.path.join(json_folder, base_filename)
    os.makedirs(output_folder, exist_ok=True)

    # Iteriere über die Frames und erstelle für jeden Frame eine Textdatei
    for frame_num, frame_data in data["projects"]["clor41l0i03gi07znfo8051e3"]["labels"][0]["annotations"]["frames"].items():

        # Definiere den vollständigen Pfad zur neuen Textdatei
        output_file = os.path.join(output_folder, f'{base_filename_cleaned}_{frame_num}.txt')

        # Öffne eine neue Textdatei für jeden Frame
        with open(output_file, 'w') as file:
            # Initialisiere den Objektzähler
            obj_counter = 0
            for obj_id, obj_data in frame_data["objects"].items():
                bbox = obj_data['bounding_box']

                # Konvertiere die Bounding-Box-Koordinaten ins YOLO-Format
                x_center, y_center, bbox_width, bbox_height = convert_coordinates(width, height, bbox)
                # Schreibe die Zeile in die YOLO-Datei
                file.write(f"{obj_counter} {x_center} {y_center} {bbox_width} {bbox_height}\n")
                # Inkrementiere den Objektzähler
                obj_counter += 1

# Schleife über alle JSON-Dateien im Ordner
for json_file in os.listdir(json_folder):
    if json_file.endswith(".json"):
        # print(json_file)
        create_yolo_labels(json_file)
