import os
from ffmpy import FFmpeg

# Erstelle das Ausgabe-Verzeichnis, falls es nicht existiert
# output_dir = "output_frames"
output_dir = "F:/GEOINFORMATIK/SEMESTER_6/Studienprojekt/output_frames"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Pfad zur Eingabe-Videodatei
# input_video = "input_video.mp4"
input_video = "F:/GEOINFORMATIK/SEMESTER_6/Studienprojekt/16mm_dvs-30_basler-70_dvs_0/16mm_dvs-30_basler-70_dvs_0/2023-09-28-botanical_garden/2023-09-28_12-16-27.479006981_dvs.mp4"
# Muster für die Ausgabe-Dateien
output_pattern = os.path.join(output_dir, "img_%04d.png")

# Erstelle das FFmpeg-Kommando
ff = FFmpeg(
    inputs={input_video: None},
    outputs={output_pattern: '-vf "fps=24"'}  # Extrahiere einen Frame pro Sekunde
)

# Führe das Kommando aus
ff.run()
