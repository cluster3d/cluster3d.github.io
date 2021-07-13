import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix
from torch.optim import SGD
from torch.optim.lr_scheduler import StepLR
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from torchvision.datasets import MNIST
from tensorboardX import SummaryWriter
import uuid

from ptdec.dec import DEC
from ptdec.model import train, predict
from ptsdae.sdae import StackedDenoisingAutoEncoder
import ptsdae.model as ae
from ptdec.utils import cluster_accuracy, custom_rand_score



from model.model_blocks import PointNet
import auxiliary.argument_parser as argument_parser


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
    return (data - torch.min(data, axis=0)[0])/(torch.max(data, axis=0)[0] + 1e-16 - torch.min(data, axis=0)[0])

class ABC2Dataset_pc(Dataset):
    """ABC2Dataset"""

    def __init__(self, root_dir,train=True, transform=None):
        """
        Args:
            root_dir (string): Directory with all the model files.
        """
        self.model_id = glob.glob(os.path.join(root_dir, '*'))
        self.root_dir = root_dir
        print("Length of model_id:", len(self.model_id))
        self.train=train
            
    def __len__(self):
        return len(self.model_id)

    def __getitem__(self, idx):

        model_ID = self.model_id[idx].split('/')[-1]

        obj_path = glob.glob(os.path.join(self.model_id[idx], '*.pt'))
        point_cloud_normalized = torch.load(obj_path[0])
        model_ID = torch.tensor(int(model_ID)).type(torch.LongTensor).cuda()
        points= norm_pc(point_cloud_normalized)
        points = points.transpose(1,0).contiguous()
        return (points, model_ID)


def main():
    cuda = True
    batch_size = 128
    opt = argument_parser.parser()
    
    print(opt)
    torch.cuda.set_device(opt.multi_gpu[0])
    hidden_dims=opt.bottleneck_size
    lr=opt.lrate
    epochs = opt.nepoch
    
    
    encoder = PointNet(nlatent=opt.bottleneck_size)
    encoder.cuda()
    
    checkpoint = torch.load("~/AtlasNet/log/atlasnet_bottleneck_size_{}/encoder.pth".format(opt.bottleneck_size))
    encoder.load_state_dict(checkpoint)
    
    writer = SummaryWriter()  # create the TensorBoard object
    # callback function to call during training, uses writer from the scope

    if cuda:
        encoder.cuda()

    ds_train = ABC2Dataset_pc("/data2/ABC2/data_raw_clustering/pc_correct_num")
    
    os.makedirs("logs/accuracy_{}_lr_{}_epochs{}/nclusters_{}/".format(hidden_dims, lr, epochs, opt.num_clusters), exist_ok=True)
    

    print("DEC stage.")
    model = DEC(cluster_number=opt.num_clusters, hidden_dimension=hidden_dims, encoder=encoder)
    if cuda:
        model.cuda()
    dec_optimizer = SGD(model.parameters(), lr=lr, momentum=0.9)
    train(
        dataset=ds_train,
        model=model,
        epochs=epochs,
        batch_size=128,
        optimizer=dec_optimizer,
        stopping_delta=0.000001,
        cuda=cuda,
        evaluate_batch_size = 64,
        output_path = "logs/accuracy_{}_lr_{}_epochs{}/nclusters_{}/".format(hidden_dims, lr, epochs, opt.num_clusters)
    )
    predicted, actual = predict(
        ds_train, model, 64, silent=True, return_actual=True, cuda=cuda
    )
    actual = actual.cpu().numpy()
    predicted = predicted.cpu().numpy()
    
    from collections import defaultdict
    import pickle
    log_clusters = {}
    for i in range(len(predicted)):
        if predicted[i] in log_clusters.keys():
            log_clusters[predicted[i]].append(actual[i])
        else:
            log_clusters[predicted[i]] = [actual[i]]
            
    accuracy = custom_rand_score(predicted, actual)
    print(accuracy)
    print("Final DEC accuracy: %s" % accuracy)
    torch.save({'model': model.state_dict()},"logs/accuracy_{}_lr_{}_epochs{}/nclusters_{}/model.pth.tar".format(hidden_dims, lr, epochs, opt.num_clusters))
    

    f=open("logs/accuracy_{}_lr_{}_epochs{}/nclusters_{}/accuracy.txt".format(hidden_dims, lr, epochs, opt.num_clusters),"w")
    f.write(str(round(accuracy, 2)))
    f.close()
    
    with open('logs/accuracy_{}_lr_{}_epochs{}/nclusters_{}/logs_clusters.pickle'.format(hidden_dims, lr, epochs, opt.num_clusters), 'wb') as handle:
        pickle.dump(log_clusters, handle)
    


if __name__ == "__main__":
    main()
