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
conda activate /home/k/kwundram/envs/yolov7

yh=/home/s/s_thie36/Projects/yolov7
tb=/scratch/tmp/s_thie36/cameratrap/training_yolo

python "$yh"/train_aux.py --workers 8 --device 0 --batch-size 8 --data "$tb"/fs_iteration.yaml --cfg "$yh"/cfg/training/yolov7-e6e-hfsp.yaml --weights "$tb"/pretrained_models/yolov7-e6e_training.pt --hyp "$yh"/data/hyp.scratch.p6-custom.yaml --single-cls --epochs 100 --img 1280 1280 --name yolov7e6e-si-multigray  --project "$tb"/runs

conda deactivate
module purge