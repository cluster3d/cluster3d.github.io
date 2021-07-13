import numpy as np
import torch
from typing import Optional
from scipy.optimize import linear_sum_assignment
from scipy.sparse import csr_matrix
from tqdm import tqdm

import time

mat = np.load('/home/desai/similarity.npz')
matrix = csr_matrix((mat['data'], mat['indices'], mat['indptr'])).toarray()
# nonzero = ground_matrix.nonzero()
indices = open("/home/desai/obj.csv","r").read().replace("\n","")
indices = np.array([int(item) for item in indices.split(",") ])
def cluster_accuracy(y_true, y_predicted, cluster_number: Optional[int] = None):
    """
    Calculate clustering accuracy after using the linear_sum_assignment function in SciPy to
    determine reassignments.

    :param y_true: list of true cluster numbers, an integer array 0-indexed
    :param y_predicted: list  of predicted cluster numbers, an integer array 0-indexed
    :param cluster_number: number of clusters, if None then calculated from input
    :return: reassignment dictionary, clustering accuracy
    """
    if cluster_number is None:
        cluster_number = (
            max(y_predicted.max(), y_true.max()) + 1
        )  # assume labels are 0-indexed
    count_matrix = np.zeros((cluster_number, cluster_number), dtype=np.int64)
    for i in range(y_predicted.size):
        count_matrix[y_predicted[i], y_true[i]] += 1

    row_ind, col_ind = linear_sum_assignment(count_matrix.max() - count_matrix)
    reassignment = dict(zip(row_ind, col_ind))
    accuracy = count_matrix[row_ind, col_ind].sum() / y_predicted.size
    return reassignment, accuracy



def custom_rand_score(y_predicted, y_true):
    """
    :param y_true: list of true cluster numbers, an integer array 0-indexed    
    :param y_true: list of model indices, an integer array 0-indexed
    """ 
    print(len(y_true))
    valid_indices = np.where(np.in1d(y_true, indices))
    y_true = y_true[valid_indices]
    y_predicted = y_predicted[valid_indices]
    
    y_true_mat = np.array([np.argwhere(indices==x) for x in y_true]).flatten()

    total = 0
    matches= 0
    counter=0
    # loop through upper triangular matrix without diagonal
    for idx_i in tqdm(range(len(y_true_mat)-1)):
        for idx_j in range(idx_i+1, len(y_true_mat)):
            counter+=1
            
            i = y_true_mat[idx_i]
            j = y_true_mat[idx_j]
            
            ground = matrix[i][j]
            if ground == 0:
                continue
            if y_predicted[idx_i] == y_predicted[idx_j]:
                pred = 1
            else:
                pred = -1
            
            if ground == pred:
                matches +=1
            total +=1
                    
    accuracy = matches/float(total)
    print(total, matches, len(y_true), counter)
    return accuracy

    
    
    
def custom_balanced_rand_score(y_predicted, y_true):
    """
    :param y_true: list of true cluster numbers, an integer array 0-indexed    
    :param y_true: list of model indices, an integer array 0-indexed
    """ 
    print(len(y_true))
    valid_indices = np.where(np.in1d(y_true, indices))
    y_true = y_true[valid_indices]
    y_predicted = y_predicted[valid_indices]
    
    y_true_mat = np.array([np.argwhere(indices==x) for x in y_true]).flatten()

    total_sim = 0
    total_dissim = 0
    matches_sim = 0
    matches_dissim = 0
    counter=0
    total=0
    # loop through upper triangular matrix without diagonal
    for idx_i in tqdm(range(len(y_true_mat)-1)):
        for idx_j in range(idx_i+1, len(y_true_mat)):
            counter+=1
            
            i = y_true_mat[idx_i]
            j = y_true_mat[idx_j]
            
            ground = matrix[i][j]
            if ground == 0:
                continue
            if y_predicted[idx_i] == y_predicted[idx_j]:
                pred = 1
            else:
                pred = -1
            
            if ground == pred and ground ==1:
                matches_sim +=1
                
            if ground==1:
                total_sim +=1
                
            if ground == pred and ground ==-1:
                matches_dissim +=1  
                
            if ground == -1:
                total_dissim +=1
            total +=1
                    
    accuracy = matches_sim*0.5/float(total_sim) + matches_dissim*0.5/float(total_dissim)
    print("similar objs: {}/{}".format(matches_sim, total_sim))
    print("dissimilar objs: {}/{}".format(matches_dissim, total_dissim))
    print("acc: {}".format(accuracy))
    return accuracy    

def target_distribution(batch: torch.Tensor) -> torch.Tensor:
    """
    Compute the target distribution p_ij, given the batch (q_ij), as in 3.1.3 Equation 3 of
    Xie/Girshick/Farhadi; this is used the KL-divergence loss function.

    :param batch: [batch size, number of clusters] Tensor of dtype float
    :return: [batch size, number of clusters] Tensor of dtype float
    """
    weight = (batch ** 2) / torch.sum(batch, 0)
    return (weight.t() / torch.sum(weight, 1)).t()
