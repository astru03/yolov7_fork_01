#!/bin/bash
 
#SBATCH --nodes=1                   # the number of nodes you want to reserve
#SBATCH --ntasks-per-node=1         # the number of tasks/processes per node
#SBATCH --cpus-per-task=36          # the number cpus per task
#SBATCH --partition=normal          # on which partition to submit the job
#SBATCH --time=24:00:00             # the max wallclock time (time limit your job will run)
 
#SBATCH --job-name=MyJob123         # the name of your job
#SBATCH --mail-type=ALL             # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user=your_account@uni-muenster.de # your mail address
 
# LOAD MODULES HERE IF REQUIRED
# module load ...
# START THE APPLICATION