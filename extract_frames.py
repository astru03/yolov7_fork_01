import os
from ffmpy import FFmpeg

# Pfad zum Ordner mit den Videodateien
video_folder = "F:/GEOINFORMATIK/SEMESTER_6/Studienprojekt/16mm_dvs-30_basler-70_dvs_0/16mm_dvs-30_basler-70_dvs_0/2023-09-28-botanical_garden"

# Ausgabe-Verzeichnis
output_base_dir = "F:/GEOINFORMATIK/SEMESTER_6/Studienprojekt/output_frames"

# Erstelle das Ausgabe-Verzeichnis, falls es nicht existiert
if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

# Schleife über alle Videodateien im angegebenen Ordner
for video_file in os.listdir(video_folder):
    if video_file.endswith(".mp4"):  # Nur .mp4-Dateien verarbeiten
        video_file_path = os.path.join(video_folder, video_file)
        
        # Extrahiere den Basename der Videodatei (ohne Pfad und Erweiterung)
        base_name = os.path.splitext(video_file)[0]
        
        # Entferne das Suffix '_dvs' vom Basename
        if base_name.endswith("_dvs"):
            base_name = base_name[:-4]
        
        # Erstelle einen spezifischen Ordner für die Frames dieser Videodatei
        output_dir = os.path.join(output_base_dir, base_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Muster für die Ausgabe-Dateien
        output_pattern = os.path.join(output_dir, f"{base_name}_%04d.png")

        # Erstelle das FFmpeg-Kommando
        ff = FFmpeg(
            inputs={video_file_path: None},
            outputs={output_pattern: '-vf "fps=1"'}  # Extrahiere Frames mit der angegebenen Framerate
        )

        # Führe das Kommando aus
        ff.run()
