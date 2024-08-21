#!/bin/bash

#SBATCH --nodes=1

#SBATCH --tasks-per-node=8

#SBATCH --partition=gpua100

#SBATCH --mem=16GB

#SBATCH --gres=gpu:1

#SBATCH --time=0-02:00:00

#SBATCH --job-name=testing_1

#SBATCH --output=/scratch/tmp/kwundram/output/testing/ins_test_1

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
# best.pt of specified training run
tested_model=/scratch/tmp/kwundram/merged_pngs_5ts/runs/yolo_ins_merged_5ts/results_export/best.pt
# test name
name="test_merged_sh_1"


# test.py on test set 
python "$yh"/test.py --data "$data" --task test --verbose --save-txt --single-cls --img 1280  --batch 6 --conf 0.001 --iou 0.65 --device 0 --weights "$tested_model"  --project /scratch/tmp/kwundram/test_results --name "$name"
