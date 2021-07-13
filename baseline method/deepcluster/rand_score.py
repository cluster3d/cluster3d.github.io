import numpy as np
from scipy.sparse import csr_matrix
from tqdm import tqdm



def custom_rand_score(y_predicted, y_true):
    """
    :param y_true: list of true cluster numbers, an integer array 0-indexed    
    :param y_true: list of model indices, an integer array 0-indexed
    """     
    mat = np.load('/home/desai/similarity.npz')
    matrix = csr_matrix((mat['data'], mat['indices'], mat['indptr'])).toarray()
    # nonzero = ground_matrix.nonzero()
    indices = open("/home/desai/obj.csv","r").read().replace("\n","")
    indices = np.array([int(item) for item in indices.split(",") ])


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
