import json
import os
import re


# Pfad zum Ordner mit den JSON-Dateien
#json_folder = r"D:\ML_INSec\data_test\annotations\output_tojson\chunkwise\2023-09-28_12-16-27.479006981"
json_folder= r"C:\Users\Andreas\Desktop\Geoinformatik\SEMESTER_6\01_Studienprojekt\annotations\Export_v2_project_ictrap_beamsplitter_4_19_2024\2023-09-28_12-16-27.479006981"

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

# Ordner 'allchunks' erstellen, falls er nicht existiert
try:
    allchunks_folder = os.path.join(json_folder, "allchunks")
    if not os.path.exists(allchunks_folder):
        os.mkdir(allchunks_folder)
        print(f"Ordner '{allchunks_folder}' erfolgreich erstellt!")
except OSError as e:
    print(f"Fehler beim Erstellen des Ordners '{allchunks_folder}': {e}")
    
# try:
#    if not os.path.exists(json_folder+"/allchunks"):
#        os.mkdir(json_folder+"/allchunks")
#        print(f"Ordner '{json_folder+"/allchunks"}' erfolgreich erstellt!")
#except OSError as e:
#    print(f"Fehler beim Erstellen des Ordners '{json_folder+"/allchunks"}': {e}")
    
#write new json file for merged id located in subfolder allchunks
with open(json_folder+"/allchunks"+f"/allchunks_{external_id_without_chunk}.json", "w") as outfile:
 json.dump({"frames":[]}, outfile)
outfile.close()
  
  
# Schleife über alle JSON-Dateien im Ordner
current_frame_count = 0
for json_file in json_list:
    if json_file.endswith(".json"):
        with open(os.path.join(json_folder, json_file), 'r') as file:
            # chunk id of current json file
            parts = json_file.split("combined_")
            chunk_id = parts[1].split("_")[0]
            chunk_id = int(chunk_id)
            # cuurent json file
            current_file = json.load(file)
            # projects id 
            projects_id = list(current_file["projects"])[0]
            # check if json has labels
            if ("labels" in current_file["projects"][projects_id] and len(current_file["projects"][projects_id]["labels"]) > 0 ):
                frames = current_file["projects"][projects_id]["labels"][0]["annotations"]["frames"]
               
                #print(f"frame content: {frames}")
                # old frame ids (string)
                frame_ids = list(frames)
                # old frame ids (int)
                ids_int_list = [int(x) for x in frame_ids]
                #print(f"Chunk number {chunk_id}: \n ")
                #print(frame_ids, "\n")
                #print(ids_int_list)
                #print (f"Difference is: {current_frame_count} \n")
                # new frame ids (int)
                ids_int_list_new = [x + current_frame_count for x in ids_int_list] 
                # new frame ids (string)
                frame_ids_new = [str(x) for x in ids_int_list_new]
                #print (frame_ids_new, "\n")
                for (old,new) in zip(frame_ids,frame_ids_new):
                    
                        #new_frame ="{'frame_ids_new':{frames[]}}"
                        old_value = frames[old]
                        frames.pop(old)
                        frames[new] = old_value
                        
                        #print(frames)
                        #print((old,new,current_frame_count))
                with open(json_folder+"/allchunks"+f"/allchunks_{external_id_without_chunk}.json", "r+") as outfile:
                    final_json= json.load(outfile)
                    
                    final_json["frames"].append(frames)
                    
                outfile.close()
                
                with open(json_folder+"/allchunks"+f"/allchunks_{external_id_without_chunk}.json", "w") as outfile:
                    json.dump(final_json,outfile, indent="")
                    
                outfile.close()
                
                    
            current_frame_count = current_frame_count + current_file["media_attributes"]["frame_count"]
                
            
            #print(f"current frame count is : {current_frame_count}")
        