import json
import cv2

# Pfad zur JSON-Datei
json_path = "C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/json_test/2023-09-28_12-16-27.479006981_combined_001_4000.mp4.json"

# JSON-Datei laden
with open(json_path, 'r') as file:
    data = json.load(file)

# Extrahieren der benötigten Werte
frame_number = "236"
bbox_data = data['projects']['clor41l0i03gi07znfo8051e3']['labels'][0]['annotations']['frames'][frame_number]['objects']
media_attributes = data['media_attributes']

# Frame Dimensionen
frame_height = media_attributes['height']
frame_width = media_attributes['width']

# URL zum Video aus der JSON-Datei extrahieren
video_url = data['data_row']['row_data']

# Video mit OpenCV laden
cap = cv2.VideoCapture(video_url)

# Überprüfen, ob das Video geöffnet werden konnte
if not cap.isOpened():
    print("Das Video konnte nicht von der URL geladen werden.")
    exit()

# Frame 236 laden
cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_number))
ret, frame = cap.read()

if not ret:
    print(f"Frame {frame_number} konnte nicht geladen werden.")
    cap.release()
    exit()

# Bounding Box Farbe und Dicke
bbox_color = (0, 255, 0)  # Grün
bbox_thickness = 2
center_color = (0, 0, 255)  # Rot
center_radius = 5
center_thickness = -1

# Funktion zum Zeichnen der Bounding-Boxen und Mittelpunkte
def draw_bounding_boxes_and_centers(bbox_data, frame):
    for obj_id, obj_data in bbox_data.items():
        bbox = obj_data['bounding_box']
        bbox_top = bbox['top']
        bbox_left = bbox['left']
        bbox_height = bbox['height']
        bbox_width = bbox['width']

        # Normierte Werte berechnen
        x_center_norm = (bbox_left + bbox_width / 2) / frame_width
        y_center_norm = (bbox_top + bbox_height / 2) / frame_height
        bbox_width_norm = bbox_width / frame_width
        bbox_height_norm = bbox_height / frame_height

        # Bounding Box Werte
        x_center = x_center_norm * frame_width
        y_center = y_center_norm * frame_height
        bbox_w = bbox_width_norm * frame_width
        bbox_h = bbox_height_norm * frame_height

        # Top-left corner
        top_left_x = int(x_center - bbox_w / 2)
        top_left_y = int(y_center - bbox_h / 2)

        # Bottom-right corner
        bottom_right_x = int(x_center + bbox_w / 2)
        bottom_right_y = int(y_center + bbox_h / 2)

        # Zeichnen der Bounding Box
        cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), bbox_color, bbox_thickness)

        # Zeichnen des Mittelpunkts
        cv2.circle(frame, (int(x_center), int(y_center)), center_radius, center_color, center_thickness)

        # Ausgabe der berechneten Bounding Box Werte
        print(f"Object ID: {obj_id}")
        print(f"  Normierter Mittelpunkt: ({x_center_norm}, {y_center_norm})")
        print(f"  Normierte Breite: {bbox_width_norm}")
        print(f"  Normierte Höhe: {bbox_height_norm}")
        print(f"  Pixel-Mittelpunkt: ({x_center}, {y_center})")
        print(f"  Pixel-Breite: {bbox_w}")
        print(f"  Pixel-Höhe: {bbox_h}")
        print(f"  Top-left corner: ({top_left_x}, {top_left_y})")
        print(f"  Bottom-right corner: ({bottom_right_x}, {bottom_right_y})\n")

# Bounding-Boxen und Mittelpunkte zeichnen und Werte ausgeben
draw_bounding_boxes_and_centers(bbox_data, frame)

# Ergebnisbild speichern
result_image_path = "C:/Users/Andreas/Desktop/result_image.png"  # Absoluter Pfad zum Speicherort und Dateinamen
cv2.imwrite(result_image_path, frame)
print(f"Das Ergebnisbild wurde als {result_image_path} gespeichert.")

cap.release()
