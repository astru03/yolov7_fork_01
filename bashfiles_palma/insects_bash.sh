#!/bin/bash

#SBATCH --nodes=1

#SBATCH --tasks-per-node=8

#SBATCH --partition=gpua100

#SBATCH --mem=48GB

#SBATCH --gres=gpu:1

#SBATCH --time=7-00:00:00

#SBATCH --job-name=insects_job

#SBATCH --output=/scratch/tmp/s_thie36/cameratrap/training_yolo/slurm_out/slurm-%j.out

#SBATCH --mail-type=ALL

#SBATCH --mail-user= kwundram@uni-muenster.de

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
tb=/scratch/tmp/kwundram/insects

data="$yh"/data/insects_pr.yaml
hyp="$yh"/data/hyp.scratch.p5_insects.yaml
weights=/scratch/tmp/kwundram/pt_weights/yolov7x.pt
cfg="$yh"/cfg/training/yolov7.yaml

# weights on github
#

python "$yh"/train.py --workers 8 --device 0 --batch-size 8 --data "$data" --cfg "$cfg"  --weights "$weights" --hyp "$hyp" --single-cls --epochs 100 --img 1280 1280 --name yolov7_insects1  --project "$tb"/runs

conda deactivate
module purge