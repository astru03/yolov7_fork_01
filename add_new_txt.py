import os

def create_missing_files(folder, start_num, end_num):
    # Überprüfe, ob der Ordner existiert
    if not os.path.exists(folder):
        print(f"Der Ordner '{folder}' existiert nicht.")
        return

    # Erstelle eine Liste mit allen vorhandenen Dateinamen im Ordner
    existing_files = os.listdir(folder)

    # Iteriere über den gewünschten Zahlenbereich
    for i in range(start_num, end_num + 1):
        # Formatiere die Dateinamen mit führenden Nullen
        filename = f"video_{str(i).zfill(5)}.txt"

        # Überprüfe, ob die Datei bereits existiert
        if filename not in existing_files:
            # Erstelle eine neue leere Datei im angegebenen Ordner
            file_path = os.path.join(folder, filename)
            with open(file_path, "w"):
                pass
            print(f"Datei '{filename}' wurde im Ordner '{folder}' erstellt.")

# Beispielaufruf
folder = r"C:\Users\Andreas\Desktop\Geoinformatik\SEMESTER_6\01_Studienprojekt\annotations\Export_v2_project_ictrap_beamsplitter_4_19_2024\2023-09-28_12-16-27.479006981\allchunks\2023-09-28_12-16-27.479006981"
create_missing_files(folder, 1, 15107)
