import os
from sklearn.model_selection import train_test_split
import argparse

# creates txt file with all absolute paths of png files in folder 
# awaits that main_folder contains subfolders with pngs
def list_png_paths(folder_path, output_file_path):
  
  png_paths = []
  for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
      # Join folder path and filename to get absolute path
      absolute_path = os.path.join(folder_path, filename)
      png_paths.append(absolute_path)

  # Open the output file in write mode
  with open( output_file_path, "a") as f:
    # Write each path to the file, followed by a newline
    f.write("\n".join(png_paths))
    f.write("\n")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--main_folder_path', type=str, required=True, help='Pfad zum Ordner mit Projektordnern')
    
    # parse arguments
    args = parser.parse_args()
    # main folder set
    main_folder_path = args.main_folder_path
    output_file_path = os.path.join(main_folder_path, "all_paths.txt")
    train_file = os.path.join(main_folder_path, "insects_train.txt")
    val_file =  os.path.join(main_folder_path, "insects_val.txt")
    
    # remove png_list if it already exists
    if os.path.exists(output_file_path):
        try:
            os.remove(output_file_path)
            print(f"File deleted: {output_file_path}")
        except OSError as e:
            print(f"Error deleting file: {output_file_path} - {e}")
    else:
        print(f"File does not exist: {output_file_path}")

    # read subfolders and read png paths 
    for subfolder in os.listdir(main_folder_path):
        # Check if the entry is a directory using os.path.isdir
        if os.path.isdir(os.path.join(main_folder_path, subfolder)):
            # project folder
            project_fodler = os.path.join(main_folder_path, subfolder)
            # get png paths in current project folder
            list_png_paths(project_fodler,output_file_path)
    print(f"PNG paths written to: {output_file_path}")

    # read all paths from created file
    with open( output_file_path, "r") as all_paths_list:
        all_lines= all_paths_list.readlines()
        # data partition
        train_set, val_set = train_test_split(all_lines, test_size=0.2, random_state=42)
        
        #training data
        with open( train_file, "w") as train_f:
            train_f.write("".join(train_set))
        train_f.close()
        # validation data
        with open( val_file, "w") as val_f:
            val_f.write("".join(val_set))
        val_f.close()
        
    all_paths_list.close()
