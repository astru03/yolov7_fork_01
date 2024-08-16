import os
from sklearn.model_selection import train_test_split
import argparse

# Erstellt eine Textdatei mit allen absoluten Pfaden der PNG-Dateien im Ordner
# Erwartet, dass main_folder Unterordner mit PNG-Dateien enthält
def list_png_paths(folder_path, output_file_path):
  
  png_paths = []
  for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
      # Fügt den Ordnerpfad und den Dateinamen zusammen, um den absoluten Pfad zu erhalten
      absolute_path = os.path.join(folder_path, filename)
      png_paths.append(absolute_path)

  # Öffnet die Ausgabedatei im Schreibmodus
  with open( output_file_path, "a") as f:
    # Schreibt jeden Pfad in die Datei, gefolgt von einem Zeilenumbruch
    f.write("\n".join(png_paths))
    f.write("\n")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--main_folder_path', type=str, required=True, help='Pfad zum Ordner mit Projektordnern')
    
    # Argumente parsen
    args = parser.parse_args()
    # Hauptordner festlegen
    main_folder_path = args.main_folder_path
    output_file_path = os.path.join(main_folder_path, "all_paths_test.txt")
    
    # PNG-Liste löschen, falls sie bereits existiert
    if os.path.exists(output_file_path):
        try:
            os.remove(output_file_path)
            print(f"File deleted: {output_file_path}")
        except OSError as e:
            print(f"Error deleting file: {output_file_path} - {e}")
    else:
        print(f"File does not exist: {output_file_path}")

    # Unterordner durchlesen und PNG-Pfade auslesen 
    for subfolder in os.listdir(main_folder_path):
        # Überprüfen, ob der Eintrag ein Verzeichnis ist, mithilfe von os.path.isdir
        if os.path.isdir(os.path.join(main_folder_path, subfolder)):
            # Projektordner
            project_fodler = os.path.join(main_folder_path, subfolder)
            # PNG-Pfade im aktuellen Projektordner abrufen
            list_png_paths(project_fodler,output_file_path)
    print(f"PNG paths written to: {output_file_path}")

