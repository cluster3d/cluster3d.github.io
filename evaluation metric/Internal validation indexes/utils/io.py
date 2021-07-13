import os
import numpy as np
import pickle
import scipy.sparse as sp


def load_obj(name, obj_dir):
    filepath = os.path.join(obj_dir, name)
    if len(name.split('.')) == 1:
        filepath += '.pkl'
    with open(filepath, 'rb') as f:
        return pickle.load(f)
    
    
def save_obj(obj, name, obj_dir):
    filepath = os.path.join(obj_dir, name)
    if len(name.split('.')) == 1:
        filepath += '.pkl'
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    

def load_file(filename, file_dir, load_type=None):
    if filename == "name_index" or load_type == 'pkl':
        return load_obj(filename, file_dir)
    elif filename == "index_name":
        return np.load(os.path.join(file_dir, filename + '.npy'), allow_pickle=True)


def load_distance_matrix(filename, file_dir):
    postfix = filename.split('.')[-1]
    if postfix == 'npz':
        file = np.load(os.path.join(file_dir, filename), allow_pickle=True)
        n = file['shape'][0]
        distance_matrix = sp.csr_matrix((file['data'], file['indices'], file['indptr']),
                                        shape=(n, n)
                                        )
        distance_matrix = distance_matrix.todense()
        distance_matrix = distance_matrix + distance_matrix.transpose()
        return distance_matrix
    elif postfix == 'npy':
        temp = np.load(os.path.join(file_dir, filename), allow_pickle=True).item()
        temp = temp.todense()
        n = len(temp)
        iou_distance = np.zeros((n,n))
        iou_distance[:temp.shape[0],:temp.shape[1]] = temp
        iou_distance += iou_distance.transpose()
        iou_distance = 1 - iou_distance
        iou_distance -= np.eye(n)
        return iou_distance
    

