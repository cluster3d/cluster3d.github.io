import os, glob
import pickle
import sys
import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset
from utils.mypath import MyPath
from torchvision.datasets.utils import check_integrity, download_and_extract_archive

def norm_pc(data):
    # print((torch.max(data, axis=0)[0] - torch.min(data, axis=0)[0]))
    return (data - torch.min(data, axis=0)[0])/(torch.max(data, axis=0)[0] + 1e-16 - torch.min(data, axis=0)[0])
    # return data
class ABC2(Dataset):
    """ABC2Dataset"""

    def __init__(self, root_dir="/data2/ABC2/data_raw_clustering/pc_correct_num", train=True, transform=None):
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
        self.transform = transform
        
        

    def __len__(self):
        return len(self.model_id)

    def __getitem__(self, idx):

        "Clustering"
        model_ID = self.model_id[idx].split('/')[-1]

        obj_path = glob.glob(os.path.join(self.model_id[idx], '*.pt'))
        # return numpy array
        points = torch.load(obj_path[0])
        model_ID = torch.tensor(int(model_ID)).type(torch.LongTensor)#.cuda()
        
        
        point_cloud= norm_pc(points)
        points = point_cloud.transpose(1,0).contiguous()
        
        
        out = {'image': points, 'target': model_ID}
    
#         if self.transform is not None:
#             out = self.transform(out)
            
        return out
    
