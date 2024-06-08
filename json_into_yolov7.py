import json
import os
import re

# Pfad zum Ordner mit den JSON-Dateien
#json_folder = "C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/json_test"
json_folder = r"D:\ML_INSec\data_test\annotations\output_tojson\test_export_result_38k_kb"
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
def create_yolo_labels(json_file,projects_id):
    with open(os.path.join(json_folder, json_file), 'r') as file:
        data = json.load(file)

    # Extrahiere Metadaten
    height = data['media_attributes']['height']  # Orginal Höhe von dvs ist 720 px
    width = data['media_attributes']['width']
    # Extrahiere den Basename der JSON-Datei (ohne Pfad und Erweiterung)
    base_filename = os.path.splitext(json_file)[0]
    print("base_filename:\n", base_filename )
    # Entferne das Suffix '_combined_###_####.mp4' aus dem Basename
    base_filename_cleaned = re.sub(r'_combined_\d+_\d+\.mp4', '', base_filename)
    print(base_filename_cleaned , "\n")

    # Erstelle einen Ordner für die Frames dieser JSON-Datei
    output_folder = os.path.join(json_folder, base_filename)
    os.makedirs(output_folder, exist_ok=True)

    # Iteriere über die Frames und erstelle für jeden Frame eine Textdatei
    for frame_num, frame_data in data["projects"][projects_id]["labels"][0]["annotations"]["frames"].items():
        # Bestimme die Präfixlänge basierend auf der Anzahl der Ziffern der Framenummer
        frame_num_str = str(frame_num)
        if len(frame_num_str) == 1:
            prefix = "video_0000"
        elif len(frame_num_str) == 2:
            prefix = "video_000"
        elif len(frame_num_str) == 3:
            prefix = "video_00"
        elif len(frame_num_str) == 4:
            prefix = "video_0"
        else:
            prefix = "video_"
        
        # Definiere den vollständigen Pfad zur neuen Textdatei
        output_file = os.path.join(output_folder, f'{prefix}{frame_num_str}.txt')

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
        print("------------- \n Processing...  ")
        with open(os.path.join(json_folder, json_file), 'r') as file:
            current_file = json.load(file)
        json_projects_id= list(current_file["projects"])[0]
        print("gelesene ID aus json: \n", list(current_file["projects"])[0])
        if ("labels" in current_file["projects"][json_projects_id] and len(current_file["projects"][json_projects_id]["labels"]) > 0 ):
            create_yolo_labels(json_file,json_projects_id)
        else:
            print(f"No labels in project {json_projects_id} in: \n {json_file} \n")
