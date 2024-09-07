#!/bin/bash

#SBATCH --nodes=1

#SBATCH --tasks-per-node=8

#SBATCH --partition=gpua100

#SBATCH --mem=16GB

#SBATCH --gres=gpu:1

#SBATCH --time=0-02:00:00

#SBATCH --job-name=testing_5ts

#SBATCH --output=/scratch/tmp/kwundram/output/testing/5ts_test

#SBATCH --mail-type=ALL

#SBATCH --mail-user=kwundram@uni-muenster.de



#load modules with available GPU support (this is an example, modify to your needs!)
module purge
module load palma/2021a Miniconda3/4.9.2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda deactivate
conda activate /home/k/kwundram/envs/insects_env

# place of fork in palma
yh=/home/k/kwundram/ml_insects/yolov7_fork_01
# data yaml contains test paths
data=/home/k/kwundram/ml_insects/yolov7_fork_01/data/insects_pr_merged.yaml


# project ; change
project=/scratch/tmp/kwundram/test_results/merged_test
#1
name="test_merged_with_val1"
tested_model=/scratch/tmp/kwundram/merged_pngs1/merged_pngs/runs/yolo_ins_merged_1/results_export/best.pt
python "$yh"/test.py --data "$data" --task test --verbose --save-txt --single-cls --img 1280  --batch 6 --conf 0.001 --iou 0.65 --device 0 --weights "$tested_model"  --project "$project" --name "$name"

#2
name="test_merged_with_val2"
tested_model=/scratch/tmp/kwundram/merged_pngs1/merged_pngs/runs/yolo_ins_merged_2/results_export/best.pt
python "$yh"/test.py --data "$data" --task test --verbose --save-txt --single-cls --img 1280  --batch 6 --conf 0.001 --iou 0.65 --device 0 --weights "$tested_model"  --project "$project" --name "$name"

#3
name="test_merged_with_val3"
tested_model=/scratch/tmp/kwundram/merged_pngs1/merged_pngs/runs/yolo_ins_merged_3/results_export/best.pt
python "$yh"/test.py --data "$data" --task test --verbose --save-txt --single-cls --img 1280  --batch 6 --conf 0.001 --iou 0.65 --device 0 --weights "$tested_model"  --project "$project" --name "$name"
