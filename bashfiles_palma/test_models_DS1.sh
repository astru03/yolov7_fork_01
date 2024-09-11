#!/bin/bash

#SBATCH --nodes=1

#SBATCH --tasks-per-node=8

#SBATCH --partition=gpua100

#SBATCH --mem=16GB

#SBATCH --gres=gpu:1

#SBATCH --time=0-02:00:00

#SBATCH --job-name=testing_5ts

#SBATCH --output=/scratch/tmp/a_stru03/output/testing/DS1_test

#SBATCH --mail-type=ALL

#SBATCH --mail-user=a_stru03@uni-muenster.de



#load modules with available GPU support (this is an example, modify to your needs!)
module purge
module load palma/2021a Miniconda3/4.9.2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda deactivate
conda activate /home/a/a_stru03/envs/astru

# place of fork in palma
yh=/home/a/a_stru03/ml_insects/yolov7_fork_01
# data yaml contains test paths
data=/home/a/a_stru03/ml_insects/yolov7_fork_01/data/insects_pr_astru.yaml


# project ; change
project=/scratch/tmp/a_stru03/test_results/DS1
#1
name="test_DS1_withval_1"
tested_model=/scratch/tmp/a_stru03/insects/runs/yolov7_model_astru_01/weights/best.pt
python "$yh"/test.py --data "$data" --task test --verbose --save-txt --single-cls --img 1280  --batch 6 --conf 0.001 --iou 0.65 --device 0 --weights "$tested_model"  --project "$project" --name "$name"

#2
name="test_DS1_withval_2"
tested_model=/scratch/tmp/a_stru03/insects/runs/yolov7_model_astru_02/weights/best.pt
python "$yh"/test.py --data "$data" --task test --verbose --save-txt --single-cls --img 1280  --batch 6 --conf 0.001 --iou 0.65 --device 0 --weights "$tested_model"  --project "$project" --name "$name"

#3 Kjells durchlauf
name="test_DS1_withval_3"
tested_model=/scratch/tmp/a_stru03/insects/runs/yolov7_model_kjell_03/weights/best.pt
python "$yh"/test.py --data "$data" --task test --verbose --save-txt --single-cls --img 1280  --batch 6 --conf 0.001 --iou 0.65 --device 0 --weights "$tested_model"  --project "$project" --name "$name"
