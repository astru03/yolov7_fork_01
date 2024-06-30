#!/bin/bash
 
#SBATCH --nodes=1                               # the number of nodes you want to reserve
#SBATCH --ntasks-per-node=1                     # the number of tasks/processes per node
#SBATCH --cpus-per-task=8                       # the number cpus per task
#SBATCH --partition=normal                      # on which partition to submit the job
#SBATCH --time=24:00:00                         # the max wallclock time (time limit your job will run)
 
#SBATCH --job-name=ml_insects                   # the name of your job
#SBATCH --mail-type=ALL                         # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user=kwundram@uni-muenster.de    # your mail address
 
hyp= 
# LOAD MODULES HERE IF REQUIRED
# module load ..
module purge
# --img 1280 1280
# -- workers 8 = cpuspertask
# device = 0

# START THE APPLICATION

# don't use more than 4 cores per GPU!
# don't use more than 30 GB per GPU reserved. Adjust the reserved time according to your needs.