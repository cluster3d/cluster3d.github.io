#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import csv
import torch
from pytorch3d.loss import chamfer_distance
import numpy as np
from tqdm import tqdm
import argparse
from time import process_time, time

parser = argparse.ArgumentParser()
parser.add_argument("project_dir", type=str)
parser.add_argument("data_dir", type=str, help="relative data directory path in project")
parser.add_argument("csv_dir", type=str, help="relative csv directory path in project")
parser.add_argument("-start", type=int, default=0)
parser.add_argument("-end", type=int, default=-1)
parser.add_argument("-cuda_name", type=str, default="cuda:0")
parser.add_argument("-mh", "--make_header", action="store_true")
args = parser.parse_args()

# In[2]:


project_dir = args.project_dir
data_dir = os.path.join(project_dir, args.data_dir)
csv_path = os.path.join(project_dir, args.csv_dir, "chamfer_distance_{}_{}.csv".format(args.start, args.end))
start = args.start
end = args.end
make_header = args.make_header or start == 0
cuda_name = args.cuda_name
start_time = process_time()
actual_start_time = time()
del args

# In[4]:


if torch.cuda.is_available():
    device = torch.device(cuda_name)

else:
    device = torch.device("cpu")
    print("WARNING: CPU only, this will be slow!")

# In[3]:


pc_list_full = os.listdir(data_dir)
if end == -1 or end > len(pc_list_full):
    end = len(pc_list_full)
pc_list = pc_list_full[0:end]
del pc_list_full


# In[5]:


def write_header():
    with open(csv_path, 'wt', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[''] + pc_list)
        writer.writeheader()


def write_row(row):
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def print_csv():
    with open(csv_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)


# In[6]:

if make_header:
    write_header()


# In[8]:


def normalize_pc(pc):
    min_ = torch.min(pc, axis=0)[0]
    return (pc - min_) / (torch.max(pc, axis=0)[0] - min_ + 1e-16)


def get_pc(pc_name):
    pc_dir = os.path.join(data_dir, pc_name)
    pc_path = os.path.join(pc_dir, os.listdir(pc_dir)[0])
    return normalize_pc(torch.load(pc_path)).unsqueeze(0).to(device)  # shape: torch.Size([1, 4096, 3])


# In[9]:

total_count = end-start
print_step = total_count // 10
last_time = process_time()
for idx1, pc1_name in enumerate(tqdm(pc_list[start:end], position=0, leave=True)):
    num_obj = idx1 + start
    row = [None] * (num_obj + 1)
    row[0] = pc1_name
    pc1 = get_pc(pc1_name)
    for idx2 in range(num_obj):
        pc2 = get_pc(pc_list[idx2])
        chamfer = chamfer_distance(pc1, pc2)[0].item()  # calculate chamfer distance
        row[idx2 + 1] = chamfer
    # write to csv
    write_row(row)
    if idx1 % print_step == 0:
        current_time = process_time()
        print(idx1, "of", total_count, "finished.")
        print("total time:", current_time - start_time)
        print("time for last", print_step, "iterations:", current_time - last_time)
        last_time = current_time

current_time = process_time()
print("finished! total time for all:", current_time - start_time)
print("time for last few iterations:", current_time - last_time)
print("total time for {} iterations: {}".format(end-start, time()-actual_start_time))
