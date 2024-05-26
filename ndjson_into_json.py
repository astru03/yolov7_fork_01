import os
import json

def ndjson_to_json(ndjson_file_path, output_directory):
    # existiert das Ausgabeverzeichnis? falls nicht erstelle es
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    with open(ndjson_file_path, 'r', encoding='utf-8') as ndjson_file:
        for line_number, line in enumerate(ndjson_file, start=1):
            # Parse die Zeile als JSON
            try:
                json_data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Fehler beim Parsen der Zeile {line_number}: {e}")
                continue
            
            # Erstelle den Pfad zur Ausgabedatei
            json_file_path = os.path.join(output_directory, f"json_{line_number}.json")
            
            # Schreibe das JSON-Objekt in eine Datei
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
            
            print(f"Zeile {line_number} erfolgreich in {json_file_path} geschrieben.")

# Beispielverwendung
# ndjson_datei = 'C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/test.ndjson'
# ausgabe_verzeichnis = 'C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/json_test'
# ndjson_to_json(ndjson_datei, ausgabe_verzeichnis)


# python ndjson_into_json.py --ndjson_file_path C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/test.ndjson --output_directory C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/json_test