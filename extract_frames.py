import os
from ffmpy import FFmpeg

# Pfad zum Ordner mit den Videodateien
video_folder = "G:/GEOINFORMATIK/SEMESTER_6/01_Studienprojekt/12mm_dvs-30_basler-70_dvs/12mm_dvs-30_basler-70_dvs"

# Ausgabe-Verzeichnis
output_base_dir = "G:/GEOINFORMATIK/SEMESTER_6/01_Studienprojekt/12mm_dvs-30_basler-70_dvs/output_frames"

# Erstellt das Ausgabe-Verzeichnis, falls es nicht existiert
if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

# Schleife über alle Videodateien im angegebenen Ordner
for video_file in os.listdir(video_folder):
    if video_file.endswith(".mp4"):  # Nur .mp4-Dateien werden verarbeitet
        video_file_path = os.path.join(video_folder, video_file)
        
        # Extrahiert den Base_name der Videodatei (ohne Pfad und Erweiterung)
        base_name = os.path.splitext(video_file)[0]
        
        # Entfernt das Suffix '_dvs' vom Base_name
        if base_name.endswith("_dvs"):
            base_name = base_name[:-4]
        
        # Erstellt einen spezifischen Ordner für die Frames dieser Videodatei
        output_dir = os.path.join(output_base_dir, base_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Muster für die Ausgabe-Dateien
        output_pattern = os.path.join(output_dir, "video_%05d.png")

        # Erstellt das FFmpeg-Kommando
        ff = FFmpeg(
            inputs={video_file_path: None},
            outputs={output_pattern: '-vf "fps=100"'}  # Extrahiert Frames mit der angegebenen Framerate
        )

        # Führe das Kommando aus
        ff.run()
