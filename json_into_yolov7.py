import json
import os

# Pfad zum Ordner mit den JSON-Dateien
json_folder = "C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/json_test_2"

# Pfad zum Zielordner für die .txt-Dateien
output_folder = "C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/json_test_2"

# Erstelle den Ordner, falls er nicht existiert
os.makedirs(output_folder, exist_ok=True)

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
    #print(height)
    #print(width)

    # Iteriere über die Frames und erstelle für jeden Frame eine Textdatei
    for frame_num, frame_data in data["projects"]["clor41l0i03gi07znfo8051e3"]["labels"][0]["annotations"]["frames"].items():
        #print(frame_num)

        # Definiere den vollständigen Pfad zur neuen Textdatei
        output_file = os.path.join(output_folder, f'frame_{frame_num}.txt')

        # Öffne eine neue Textdatei für jeden Frame
        with open(output_file, 'w') as file:
            for obj_id, obj_data in frame_data["objects"].items():
              #print(obj_id)
              class_id = obj_data['feature_id']
              #print(class_id)
              bbox = obj_data['bounding_box']
              #print(bbox)

              # Konvertiere die Bounding-Box-Koordinaten ins YOLO-Format
              x_center, y_center, bbox_width, bbox_height = convert_coordinates(width, height, bbox)
              # Schreibe die Zeile in die YOLO-Datei
              file.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")
 
# Schleife über alle JSON-Dateien im Ordner
for json_file in os.listdir(json_folder):
    if json_file.endswith(".json"):
        print(json_file)
        create_yolo_labels(json_file)
