import json
import os
import re


# Pfad zum Ordner mit den JSON-Dateien
json_folder = r"D:\ML_INSec\data_test\annotations\output_tojson\chunkwise\2023-09-28_12-16-27.479006981"

# merge
def merge_anno(json_file):
    with open(os.path.join(json_folder, json_file), 'r') as file:
        data = json.load(file)
        parts = json_file.split("combined_")
        
        chunk_id = parts[1].split("_")[0]
        chunk_id = int(chunk_id)
        
        print(f"{json_file} has chunk_id  {chunk_id}")
        
            
            
# list of jsons
json_list = os.listdir(json_folder)
# opens first json 

with open(os.path.join(json_folder, json_list[0]), 'r') as file:
            json_data = json.load(file)
# get external id 
external_id = json_data.get("data_row", {}).get("external_id")
if not external_id:
    print(f" keine 'external_id' in {file} \n.")
    
# get external id without chunk id
pattern = r"(.*?)_combined"
external_id_without_chunk=re.search(pattern, external_id).group(1)

try:
    if not os.path.exists(json_folder+"/allchunks"):
        os.mkdir(json_folder+"/allchunks")
        print(f"Ordner '{json_folder+"/allchunks"}' erfolgreich erstellt!")
except OSError as e:
    print(f"Fehler beim Erstellen des Ordners '{json_folder+"/allchunks"}': {e}")
    
#write new json file for merged id
with open(json_folder+"/allchunks"+f"/allchunks_{external_id_without_chunk}.json", "w") as outfile:
  outfile.write("{}")
  
  
# Schleife über alle JSON-Dateien im Ordner
current_frame_count = 0
for json_file in json_list:
    if json_file.endswith(".json"):
        with open(os.path.join(json_folder, json_file), 'r') as file:
            current_file = json.load(file)
        #print(f"jsonfile in loop: {json_file}\n")
            
            current_frame_count = current_frame_count + current_file["media_attributes"]["frame_count"]
            print(f"current frame count is : {current_frame_count}")
        merge_anno(json_file)