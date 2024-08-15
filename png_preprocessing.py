# script takes image with index n and merges with n-1th and n-2th image to BGR-image.
import os
import cv2
import numpy as np

# project folder with original video projects
project_folder = r"D:\ML_INSec\st_pr_exchange_copy"
# output folder with merged BGR images
output_folder = r"D:\ML_INSec\merged_pngs"

subfolders = []
# get all project folders with absolute path
for entry in os.listdir(project_folder):
    full_path = os.path.join(project_folder, entry)
    if os.path.isdir(full_path):
      subfolders.append(full_path)
      
# iterate over video projects
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
    
    png_list = []
    # init of empty image arrays
    im1 = np.array([])
    im2 = np.array([])
    for file in  os.listdir(vid_project):
        file_path = os.path.join(vid_project,file)
        root, ext = os.path.splitext(file_path)
        if ext ==".png":
            #print(ext)
            png_list.append(file)
            if im1.size == 0:
                im1 = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                print("im1")
                print(im1.dtype)
                print(im1.shape)
                continue
            elif im2.size == 0:
                im2 = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                print("im2")
                print(im2.dtype)
                print(im2.shape)
                continue
            else:
                im3 = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                print("im3")
                print(im3.dtype)
                print(im3.shape)
                
                merged_img = cv2.merge((im1, im2, im3)) # bgr
                cv2.imwrite(os.path.join(output_folder,project_name,file), merged_img)
                im1 = im2
                im2 = im3
                

            
            
            
    
