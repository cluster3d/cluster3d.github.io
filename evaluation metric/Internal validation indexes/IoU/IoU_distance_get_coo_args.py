#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
import os
from time import time

import numpy as np
from iou_constants import data_dir, iou_coo_args_dir, iou_coo_args_name_start_end
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("start", type=int)
parser.add_argument("end", type=int)
args = parser.parse_args()
start = args.start
end = args.end
del args

# In[3]:


start_time = time()

obj_list = sorted(os.listdir(data_dir))
if end == -1 or end > len(obj_list):
    end = len(obj_list)

n = end - start
obj_list = obj_list[:end]


# In[4]:


def iou(voxel_matrix1, voxel_matrix2):
    i = np.count_nonzero(np.logical_and(voxel_matrix1, voxel_matrix2))
    if i == 0:
        return 0
    return i / np.count_nonzero(np.logical_or(voxel_matrix1, voxel_matrix2))


# In[5]:


num_comp = (start + end - 1) * n // 2
data = np.zeros(num_comp)
ii = np.zeros(num_comp, dtype=int)
jj = np.zeros(num_comp, dtype=int)

index = 0
for idx1, obj1_name in enumerate(tqdm(obj_list[start:], position=0, leave=True), start=start):
    voxel_matrix1 = np.load(os.path.join(data_dir, obj1_name, "{}_normalized.npy".format(obj1_name)), allow_pickle=True)
    for idx2, obj2_name in enumerate(obj_list[:idx1]):
        voxel_matrix2 = np.load(os.path.join(data_dir, obj2_name, "{}_normalized.npy".format(obj2_name)), allow_pickle=True)
        #         index == (idx1-1) * idx1 // 2
        data[index] = iou(voxel_matrix1, voxel_matrix2)
        ii[index] = idx1
        jj[index] = idx2
        index += 1

# In[9]:


print("run time:", time() - start_time)

# In[18]:


np.savez(os.path.join(iou_coo_args_dir, iou_coo_args_name_start_end.format(start, end)), data=data, ii=ii, jj=jj)

# In[ ]:
