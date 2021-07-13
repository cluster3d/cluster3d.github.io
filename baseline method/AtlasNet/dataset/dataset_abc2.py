import glob
import os
import torch.nn.functional as F
import pandas as pd
import re
import ast
import torch
import numpy as np
from torch.utils.data import Dataset


"""
This is used for point cloud dataloader.
"""
def norm_pc(data):
    return (data - torch.min(data, axis=0)[0])/(torch.max(data, axis=0)[0] + 1e-16 - torch.min(data, axis=0)[0])

class ABC2Dataset_pc(Dataset):
    """ABC2Dataset"""

    def __init__(self, root_dir, train=True, transform=None):
        """
        Args:
            root_dir (string): Directory with all the model files.
        """
        self.model_id = glob.glob(os.path.join(root_dir, '*'))
        self.root_dir = root_dir
        self.train=train
        
        if self.train:
            print("indices:",0,int(0.8*len(self.model_id)))
            self.model_id = self.model_id[0:int(0.8*len(self.model_id))]
        else:
            print("indices:",int(0.8*len(self.model_id)))            
            self.model_id = self.model_id[int(0.8*len(self.model_id)):]
            
        print("model_id:", len(self.model_id))

    def __len__(self):
        return len(self.model_id)

    def __getitem__(self, idx):
        model_ID = self.model_id[idx].split('/')[-1]

        obj_path = glob.glob(os.path.join(self.model_id[idx], '*.pt'))
        point_cloud_normalized = torch.load(obj_path[0]).cuda()

        return_points = {}
        return_points['points'] = norm_pc(point_cloud_normalized)
        return return_points
