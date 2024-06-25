import json
import os
import re

# Pfad zur JSON-Datei
json_file_path = r"C:\Users\Andreas\Desktop\Geoinformatik\SEMESTER_6\01_Studienprojekt\annotations\Export_v2_project_ictrap_beamsplitter_4_19_2024\2023-09-28_12-16-27.479006981\allchunks\allchunks_2023-09-28_12-16-27.479006981.json"

# Funktion zur Konvertierung der Koordinaten in das YOLO-Format
def convert_coordinates(width, height, bbox):
    x_center = bbox['left'] + bbox['width'] / 2
    y_center = bbox['top'] + bbox['height'] / 2
    x_center /= width
    y_center /= height
    bbox_width = bbox['width'] / width
    bbox_height = bbox['height'] / height
    return x_center, y_center, bbox_width, bbox_height

# Funktion zur Erstellung der YOLO-Labels
def create_yolo_labels(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extrahiere Metadaten
    height = float(1080)
    width = float(1920)

    # Extrahiere den Basename der JSON-Datei (ohne Pfad und Erweiterung)
    base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
    base_filename = base_filename.replace("allchunks_", "")
    print("base_filename:\n", base_filename)

    # Erstelle einen Ordner für die Frames dieser JSON-Datei
    output_folder = os.path.join(os.path.dirname(json_file_path), base_filename)
    os.makedirs(output_folder, exist_ok=True)

    # Iteriere über die Frames und erstelle für jeden Frame eine Textdatei
    for frame in data["frames"]:
        for frame_num, frame_data in frame.items():
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

            # Initialisiere den Objektzähler
            obj_counter = 0
            yolo_lines = []

            for obj_id, obj_data in frame_data["objects"].items():
                # Abfrage ob "name":"insect" und "value":"insect"
                if obj_data.get("name") == "insect" and obj_data.get("value") == "insect":
                    bbox = obj_data['bounding_box']
                    # Konvertiere die Bounding-Box-Koordinaten ins YOLO-Format
                    x_center, y_center, bbox_width, bbox_height = convert_coordinates(width, height, bbox)
                    # Füge die Zeile zur Liste hinzu
                    yolo_lines.append(f"{obj_counter} {x_center} {y_center} {bbox_width} {bbox_height}")
                    # Inkrementiere den Objektzähler
                    obj_counter += 1

            # Schreibe nur dann eine Datei, wenn es mindestens eine gültige Objektzeile gibt.
            if yolo_lines:
                output_file = os.path.join(output_folder, f'{prefix}{frame_num_str}.txt')
                with open(output_file, 'w') as file:
                    file.write("\n".join(yolo_lines))

# Erstelle YOLO-Labels für die gegebene JSON-Datei
create_yolo_labels(json_file_path)
