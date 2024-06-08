#Nummeriert die txt-Datein neun, wenn es sich bei der Labelbox-Annotation um mehrere Stücke handelt in denen immer 4000 Frames vorhanden sind.
# Dieses Skript gilt dann für die Ordner "combined_001_4000", "combined_002_4000", "combined_003_3107 usw. 
# Vorsicht! Bei der letzten Datein mit 003 Darauf achten, dass es nicht immer bis Frame 4000 geht
import os

def rename_files(folder_path, start_num):
    # Überprüfe, ob der Ordnerpfad existiert
    if not os.path.exists(folder_path):
        print(f"Der Ordner '{folder_path}' existiert nicht.")
        return

    # Erstelle eine Liste mit allen TXT-Dateien im Ordner
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # Sortiere die Liste, um eine konsistente Reihenfolge zu gewährleisten
    txt_files.sort()

    # Iteriere über die TXT-Dateien und setze die Nummerierung neu
    for i, filename in enumerate(txt_files, start=start_num):
        old_path = os.path.join(folder_path, filename)
        new_filename = f"video_{i}.txt"
        new_path = os.path.join(folder_path, new_filename)

        # Benenne die Datei um
        os.rename(old_path, new_path)
        print(f"Datei '{filename}' wurde in '{new_filename}' umbenannt.")

# Beispielaufruf
folder_path = "C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/json_test/2023-09-28_12-16-27.479006981_combined_003_3107.mp4"
start_num = 12001 # Diese nummer jedes mal anpassen und schauen bei welchem Frame das nächste Stück beginnen soll. Bei "combined_001_4000" startet die nummerierung bei 4001, bei "combined_002_4000" startet die Nummerierung bei 8001 und bei "combined_003_3107" startet die Nummerierung bei 12001
rename_files(folder_path, start_num)