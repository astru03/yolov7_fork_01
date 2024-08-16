import json
import os
import re


# Pfad zum Ordner mit den JSON-Dateien
# json_folder = r"D:\ML_INSec\data_test\annotations\output_tojson\chunkwise\2023-09-28_12-16-27.479006981"
json_folder= r"C:\Users\Andreas\Desktop\Geoinformatik\SEMESTER_6\01_Studienprojekt\annotations\Export_v2_project_ictrap_beamsplitter_8_12_2024\2023-10-15_13-28-13.077287350"

# Liste der JSON-Dateien im Ordner
json_list = os.listdir(json_folder)

# Öffnen der ersten JSON-Datei
with open(os.path.join(json_folder, json_list[0]), 'r') as file:
            json_data = json.load(file)
            
# Abrufen der 'external_id' aus der ersten JSON-Datei
external_id = json_data.get("data_row", {}).get("external_id")
if not external_id:
    print(f" keine 'external_id' in {file} \n.")
    
# Entfernen der Chunk-ID aus der 'external_id'. In diesem fall die Bezeichnung mit "_combined"
pattern = r"(.*?)_combined"
external_id_without_chunk=re.search(pattern, external_id).group(1)

#  Ordner 'allchunks' erstellen, falls dieser nicht existiert. In diesem wird die zusammengesetzte neue JSON-Datei abgespeichert
try:
    allchunks_folder = os.path.join(json_folder, "allchunks")
    if not os.path.exists(allchunks_folder):
        os.mkdir(allchunks_folder)
        print(f"Ordner '{allchunks_folder}' erfolgreich erstellt!")
except OSError as e:
    print(f"Fehler beim Erstellen des Ordners '{allchunks_folder}': {e}")

# Neue JSON-Datei für die zusammengeführten Daten erstellen und in den Unterordner 'allchunks' speichern
with open(json_folder+"/allchunks"+f"/allchunks_{external_id_without_chunk}.json", "w") as outfile:
 json.dump({"frames":[]}, outfile)
outfile.close()
  
# Schleife über alle JSON-Dateien im Ordner
current_frame_count = 0
for json_file in json_list:
    if json_file.endswith(".json"):
        with open(os.path.join(json_folder, json_file), 'r') as file:
            # Chunk-ID der aktuellen JSON-Datei ermitteln
            parts = json_file.split("combined_")
            chunk_id = parts[1].split("_")[0]
            chunk_id = int(chunk_id)
            # Laden der aktuellen JSON-Datei
            current_file = json.load(file)
            # Projekt-ID ermitteln
            projects_id = list(current_file["projects"])[0]
            # Überprüfen, ob Labels in der JSON-Datei vorhanden sind
            if ("labels" in current_file["projects"][projects_id] and len(current_file["projects"][projects_id]["labels"]) > 0 ):
                frames = current_file["projects"][projects_id]["labels"][0]["annotations"]["frames"]
                # Alte Frame-IDs (als String und als Integer)
                frame_ids = list(frames)
                ids_int_list = [int(x) for x in frame_ids]
 
                # Berechnen der neuen Frame-IDs, indem die aktuelle Frame-Anzahl hinzugefügt wird
                ids_int_list_new = [x + current_frame_count for x in ids_int_list] 
                frame_ids_new = [str(x) for x in ids_int_list_new]
                
                # Ersetzen der alten Frame-IDs durch die neuen IDs
                for (old,new) in zip(frame_ids,frame_ids_new):
                        old_value = frames[old]
                        frames.pop(old)
                        frames[new] = old_value
                        
                # Laden der JSON-Datei, in der alle Chunks zusammengeführt werden sollen
                with open(json_folder+"/allchunks"+f"/allchunks_{external_id_without_chunk}.json", "r+") as outfile:
                    final_json= json.load(outfile)
                     # Anhängen der Frames des aktuellen Chunks an die endgültige JSON-Datei
                    final_json["frames"].append(frames)
                outfile.close()

                # Speichern der aktualisierten JSON-Datei
                with open(json_folder+"/allchunks"+f"/allchunks_{external_id_without_chunk}.json", "w") as outfile:
                    json.dump(final_json,outfile, indent="")
                outfile.close()

            # Aktualisieren der aktuellen Frame-Anzahl um die Anzahl der Frames im aktuellen Chunk   
            current_frame_count = current_frame_count + current_file["media_attributes"]["frame_count"]
        