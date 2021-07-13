from __future__ import print_function, division

import glob
import os
import torch
from torch.utils.data import Dataset
import torch.nn.functional as F
import pandas as pd
import numpy as np
import re
import ast

"""
This is used for point cloud dataloader.
"""
def norm_pc(data):
    # print((torch.max(data, axis=0)[0] - torch.min(data, axis=0)[0]))
    return (data - torch.min(data, axis=0)[0])/(torch.max(data, axis=0)[0] + 1e-16 - torch.min(data, axis=0)[0])
    # return data

    
class ABC2Dataset_pc(Dataset):
    """ABC2Dataset"""

    def __init__(self, root_dir):
        """
        Args:
            root_dir (string): Directory with all the model files.
        """
        self.model_id = glob.glob(os.path.join(root_dir, '*'))
        self.root_dir = root_dir
        self.pc = self.point_cloud()

    def __len__(self):
        return len(self.model_id)

    def __getitem__(self, idx):

        """Clustering"""
        model_ID = self.model_id[idx].split('/')[-1]
        # if string_label is np.nan:
        #     print("%d has no label for Clustering" % idx)
        # else:
        obj_path = glob.glob(os.path.join(self.model_id[idx], '*.pt'))
        point_cloud_normalized = torch.load(obj_path[0])
        return (norm_pc(point_cloud_normalized), model_ID)

    def point_cloud(self):
        """
        Args: root with point cloud; class index
        Return: a list of tuple; each tuple: ('point cloud path', 0)
        mimic the datasets.ImageFolder in torchvision.datasets
        """
        # import pdb;pdb.set_trace()
        pc_folder_path = self.model_id
        num_folder = len(pc_folder_path)
        pc_all = []
        for i in range(num_folder):
            pc_path = glob.glob(os.path.join(pc_folder_path[i], '*.pt'))
            # print("pc_path:", pc_path)
            pc_path_with_zero = (pc_path, 0)
            pc_all.append(pc_path_with_zero)
        return pc_all


        


