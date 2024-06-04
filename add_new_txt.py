import os

def create_missing_files(parent_folder, start_num, end_num):
    # Überprüfe, ob der übergeordnete Ordnerpfad existiert
    if not os.path.exists(parent_folder):
        print(f"Der Ordner '{parent_folder}' existiert nicht.")
        return

    # Iteriere über alle Unterordner im übergeordneten Ordner
    for subfolder in os.listdir(parent_folder):
        subfolder_path = os.path.join(parent_folder, subfolder)

        # Überprüfe, ob der aktuelle Eintrag ein Ordner ist
        if os.path.isdir(subfolder_path):
            # Erstelle eine Liste mit allen vorhandenen Dateinamen im Unterordner
            existing_files = os.listdir(subfolder_path)

            # Iteriere über den gewünschten Zahlenbereich
            for i in range(start_num, end_num + 1):
                # Formatiere die Dateinamen mit führenden Nullen
                filename = f"video_{str(i).zfill(5)}.txt"

                # Überprüfe, ob die Datei bereits existiert
                if filename not in existing_files:
                    # Erstelle eine neue leere Datei im angegebenen Unterordner
                    file_path = os.path.join(subfolder_path, filename)
                    with open(file_path, "w"):
                        pass
                    print(f"Datei '{filename}' wurde in '{subfolder}' erstellt.")

# Beispielaufruf
parent_folder = "C:/Users/Andreas/Desktop/Geoinformatik/SEMESTER_6/01_Studienprojekt/annotations/json_test"
create_missing_files(parent_folder, 1, 4000)