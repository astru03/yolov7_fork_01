#!/bin/bash

#SBATCH --nodes=1

#SBATCH --tasks-per-node=8

#SBATCH --partition=gpua100

#SBATCH --mem=20GB

#SBATCH --gres=gpu:1

#SBATCH --time=7-00:00:00

#SBATCH --job-name=insects_job_merged_5ts_1

#SBATCH --output=/scratch/tmp/kwundram/output/insects_merged_5ts_1

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
# folder with project folders containing pngs and txts
tb=/scratch/tmp/kwundram/merged_pngs_5ts
# data yaml contains absolute paths and needs to be changed
data="$yh"/data/insects_pr_merged_5ts.yaml
# hyp stays same 
hyp="$yh"/data/hyp.scratch.p5_insects.yaml
#yolov7x weights
weights=/scratch/tmp/kwundram/pt_weights/yolov7x.pt
# yolov7x yaml stays same
cfg="$yh"/cfg/training/yolov7x.yaml
name="yolo_ins_merged_5ts"

# weights on github
#

python "$yh"/train.py --workers 4 --device 0 --batch-size 6 --data "$data" --cfg "$cfg"  --weights "$weights" --hyp "$hyp" --single-cls --epochs 80 --img 1280 1280 --name "$name"  --project "$tb"/runs

conda deactivate
module purge