import os
import json
import argparse
import re

def ndjson_to_json(ndjson_file_path, output_directory):
    # Existiert das Ausgabeverzeichnis? Falls nicht, erstelle es.
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
            
            # Extrahiere den Wert des Feldes "external_id"
            external_id = json_data.get("data_row", {}).get("external_id")
            if not external_id:
                print(f"Zeile {line_number} enthält kein 'external_id' Feld.")
                continue
            # putting chunks of same video in one folder
            pattern = r"(.*?)_combined"
            external_id_without_chunk=re.search(pattern, external_id).group(1)
            # Ordner erstellen
            try:
                if not os.path.exists(os.path.join(output_directory,external_id_without_chunk)):
                    os.mkdir(os.path.join(output_directory,external_id_without_chunk))
                    print(f"Ordner '{os.path.join(output_directory,external_id_without_chunk)}' erfolgreich erstellt!")
            except OSError as e:
                print(f"Fehler beim Erstellen des Ordners '{os.path.join(output_directory,external_id_without_chunk)}': {e}")
                
            # Erstelle den Pfad zur Ausgabedatei unter Verwendung von "external_id"
            json_file_path = os.path.join(output_directory,external_id_without_chunk,f"{external_id}.json")
            
            # Schreibe das JSON-Objekt in eine Datei
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
            
            print(f"Zeile {line_number} erfolgreich in {json_file_path} geschrieben.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Konvertiere NDJSON zu JSON Dateien.')
    parser.add_argument('--ndjson_file_path', type=str, required=True, help='Pfad zur NDJSON Datei')
    parser.add_argument('--output_directory', type=str, required=True, help='Ausgabeverzeichnis für JSON Dateien')

    args = parser.parse_args()
    
    ndjson_to_json(args.ndjson_file_path, args.output_directory)
