#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from math import sqrt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("project_dir", type=str)
parser.add_argument("data_dir", type=str, help="relative data directory path in project")
parser.add_argument("sbatch_dir", type=str, help="relative sbatch directory path in project")
parser.add_argument("num_jobs", type=int, help="number of jobs")
parser.add_argument("-start", type=int, default=0)
parser.add_argument("-end", type=int, default=-1)
parser.add_argument("-gpu", type=str, default="rtx8000")
parser.add_argument("-time", type=str, default="23:59:59")
args = parser.parse_args()


# In[12]:


start = args.start
end = args.end
num_jobs = args.num_jobs
data_dir = os.path.join(args.project_dir, args.data_dir)
sbatch_dir = os.path.join(args.project_dir, args.sbatch_dir)
gpu_type = args.gpu
run_time = args.time
del args

# In[13]:


num_files = len(os.listdir(data_dir))
if end < start:
    end = num_files


# In[14]:


def sbatch_from_template(num_jobs):
    comp_count = (start + end - 2) * (end - start) / 2
    comp_perjob = comp_count / num_jobs
    jstart = start
    for jobi in range(num_jobs):
        jend = int(sqrt(jstart*jstart+comp_perjob))
        if jend <= jstart:
            print("same start and end at job", jobi)
            continue
        if jend >= num_files:
            jend = num_files
        content = "#!/bin/bash -e\n" \
                  "#\n" \
                  "#SBATCH --nodes=1\n" \
                  "#SBATCH --ntasks-per-node=1\n" \
                  "#SBATCH --cpus-per-task=2\n" \
                  "#SBATCH --time={}\n" \
                  "#SBATCH --mem=10GB\n" \
                  "#SBATCH --job-name=chamfer_distance_{}-{} \n" \
                  "#SBATCH --mail-user=yk1962@nyu.edu \n" \
                  "#SBATCH --output=/scratch/yk1962/ABC/output/slurm_%j_{}_{}.out\n" \
                  "#SBATCH --gres=gpu:{}:1\n" \
                  "\n" \
                  "module purge\n" \
                  "\n" \
                  "# Enter required modules\n" \
                  "\n" \
                  "# Execute Commands\n" \
                  "cd /scratch/yk1962/ABC/code\n" \
                  "source /scratch/yk1962/miniconda3/bin/activate pytorch3d\n" \
                  "# conda activate pytorch3d \n" \
                  "python chamfer_distance.py /scratch/yk1962/ABC data/pc_correct_num_40960 result -start={} -end={} -cuda_name=cuda:0\n"
        content = content.format(run_time, jstart, jend, jstart, jend, gpu_type, jstart, jend)
        with open(os.path.join(sbatch_dir, "job{}.sh".format(jobi)), "w") as f:
            f.write(content)
        if jend >= num_files:
            break
        jstart = jend


# In[15]:


sbatch_from_template(num_jobs)


# In[ ]:




