#!/bin/bash

#SBATCH --nodes=1

#SBATCH --tasks-per-node=8

#SBATCH --partition=gpua100

#SBATCH --mem=32GB

#SBATCH --gres=gpu:1

#SBATCH --time=7-00:00:00

#SBATCH --error=/scratch/tmp/a_stru03/errors/insects

#SBATCH --job-name=insects_job

#SBATCH --output=/scratch/tmp/a_stru03/output/insects

#SBATCH --mail-type=ALL

#SBATCH --mail-user= a_stru03@uni-muenster.de

#load modules with available GPU support (this is an example, modify to your needs!)
module purge
module load palma/2021a Miniconda3/4.9.2

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh
conda deactivate
conda activate /home/a/a_stru03/envs/astru

# place of fork in palma
yh=/home/a/a_stru03/ml_insects/yolov7_fork_01
# folder with project folders containing pngs and txts
tb=/scratch/tmp/a_stru03/insects
data="$yh"/data/insects_pr_astru.yaml
hyp="$yh"/data/hyp.scratch.p5_insects.yaml
#yolov7x weights
weights=/scratch/tmp/a_stru03/pt_weights/yolov7x.pt
# yolov7x yaml
cfg="$yh"/cfg/training/yolov7x.yaml
name="yolov7_modell"
# weights on github
#

python "$yh"/train.py --workers 4 --device 0 --batch-size 6 --data "$data" --cfg "$cfg"  --weights "$weights" --hyp "$hyp" --single-cls --epochs 100 --img 1280 1280 --name "$name" --project "$tb"/runs

conda deactivate
module purge