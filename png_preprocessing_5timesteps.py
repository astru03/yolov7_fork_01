import os
import cv2
import numpy as np
import shutil

def copy_file(source_file, destination_folder):

  
  with open (destination_folder,"w+") as f:
   
    shutil.copy2(source_file, destination_folder)
  
  
# function takes index_before and index_after to search for successor and predeccessor image and merge them with current image
# if current image is video_00006.png and index_before = 5 and index_after = 5 then:
#   successor is video_00011.png and predeccessor is video_00001.png
def take_additional_timesteps(project_folder,output_folder,index_before:int,index_after:int):
    if  not os.path.exists(output_folder):
                os.mkdir(output_folder)
    subfolders = []
    # get all project folders with absolute path
    for entry in os.listdir(project_folder):
        full_path = os.path.join(project_folder, entry)
        if os.path.isdir(full_path):
            subfolders.append(full_path)
    
    # iterate over video projects
    # subfolders contains absolute paths
    for vid_project in subfolders:
        # e.g 2023-09-28_12-16-27.479006981
        project_name = os.path.basename(vid_project)
        # create project folder in output folder
        try:
            output_project = os.path.join(output_folder,project_name)
            if  not os.path.exists(output_project):
                os.mkdir(output_project)
        except Exception:
            print("could not create project folder in output folder")
            
        for file in  os.listdir(vid_project):
            file_path = os.path.join(vid_project,file)
            root, ext = os.path.splitext(file_path)
            
            if ext ==".png":
                index_string = os.path.basename(root)
                #print(index_string)
                index = index_string.split("_")[1]
                index_int = int(index)
                #print(index)
                #  index of successor image
                new_index_after = str(index_int + index_after).zfill(len(index))
                #print("new_index_after",new_index_after)
                # index of predecessor image
                new_index_before = str(index_int - index_before).zfill(len(index))
                #print("new_index_before",new_index_before)
                
                # check if successor exists
                successor_path = os.path.join(vid_project,"video_"+new_index_after+".png")
                #print(successor_path)
                if os.path.exists(successor_path):
                    #print("successor exists")
                    im1= cv2.imread(successor_path, cv2.IMREAD_GRAYSCALE)
                else:
                    im1 = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                    #print("successor  does not exist")
                    
                # check if predecessor exists
                predecessor_path = os.path.join(vid_project,"video_"+new_index_before+".png")
                #print(predecessor_path)
                if os.path.exists(predecessor_path):
                    #print("predecessor exists")
                    im3 = cv2.imread(predecessor_path, cv2.IMREAD_GRAYSCALE)
                else:
                    im3 = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                    #print("predecessor does not exist")
                
                # im2 is always current image
                im2 = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if len(im1.shape) > 2   or len(im2.shape) > 2 or len(im3.shape) > 2:
                    print(f"more channels in  {file_path}?")
                
                merged_img = cv2.merge((im1, im2, im3)) # bgr
                cv2.imwrite(os.path.join(output_folder,project_name,file), merged_img)
            
            if ext ==".txt":
                copy_file(file_path,os.path.join(output_project,file))
                print(file_path,"copied to",os.path.join(output_project,file))
                #print("---------")
                
                
        
            
# project folder with original video projects
project_folder = r"D:\ML_INSec\st_pr_exchange_copy"
# output folder with merged BGR images
output_folder = r"D:\ML_INSec\merged_pngs_2"
take_additional_timesteps(project_folder,output_folder,5,5)
      
