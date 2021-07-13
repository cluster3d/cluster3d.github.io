import numpy as np
from tqdm import tqdm
import csv
from scipy.sparse import csr_matrix

def read_similarity_matrix(filename):
    mat = np.load(filename)
    return csr_matrix((mat['data'], mat['indices'], mat['indptr'])).toarray()

def read_predict_cluster_file(filename):
    obj_list = []
    with open('obj.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, quotechar='|')
        for row in spamreader:
            obj_list = row

    obj_dict = {}
    for i, obj in enumerate(obj_list):
        obj_dict[obj] = i

    model_ids = []
    predict_cluster = []
    
    with open(filename, "r") as f:
        file_contents = f.read()
        contents_split = file_contents.splitlines()
        for line in contents_split:
            row = line.split(', ')
            model_ids.append(row[0].zfill(8))
            predict_cluster.append(int(row[1]))
    
    cluster_result = []
    k = int(filename.split('/')[1])
    for i in range(k):
        cluster_result.append([])
    for i, cluster in enumerate(predict_cluster):
        if model_ids[i] in obj_dict:
            cluster_result[cluster].append(obj_dict[model_ids[i]])

    return cluster_result

def pairwise_purity(cluster_result, similarity_matrix):
    cluster_dict = {}
    for cluster_idx, cluster in enumerate(cluster_result):
        for obj_idx in cluster:
            cluster_dict[obj_idx] = cluster_idx
            
    model_idx_list = [item for sublist in cluster_result for item in sublist]
    
    total_edges_cnt = 0
    correct_predict_edge_cnt = 0
    for idx, model_idx_i in enumerate(tqdm(model_idx_list)):
        for model_idx_j in model_idx_list[idx:]:
            ground_truth = similarity_matrix[model_idx_i][model_idx_j]
            if ground_truth == 0:
                continue
            elif ground_truth == 1:
                if cluster_dict[model_idx_i] == cluster_dict[model_idx_j]:
                    correct_predict_edge_cnt += 1
            elif ground_truth == -1:
                if cluster_dict[model_idx_i] != cluster_dict[model_idx_j]:
                    correct_predict_edge_cnt += 1
            total_edges_cnt += 1
    
    return correct_predict_edge_cnt/total_edges_cnt

def inter_class_purity(cluster_result, similarity_matrix):
    idx = 0
    total_edge_cnt = 0
    purity = 0
    for cluster_u in tqdm(cluster_result):
        for cluster_v in cluster_result[idx+1:]:
            miscluster_cnt = 0
            cross_cluster_cnt = 0
            for u in cluster_u:
                for v in cluster_v:
                    if similarity_matrix[u][v] == 1:
                        miscluster_cnt += 1
                    elif similarity_matrix[u][v] == -1:
                        cross_cluster_cnt += 1

            total_edge_cnt += miscluster_cnt+cross_cluster_cnt
            purity += cross_cluster_cnt
        idx += 1

    return purity/total_edge_cnt

def intra_class_purity(cluster_result, similarity_matrix):
    total_cluster_cnt = 0
    purity = 0
    for cluster in tqdm(cluster_result):
        if len(cluster) == 0 or len(cluster) == 1:
            continue
        cluster_similarity = similarity_matrix[cluster,:][:,cluster]
        similar_edge_count = np.count_nonzero(cluster_similarity == 1) - len(cluster)
        total_edge_count = similar_edge_count + np.count_nonzero(cluster_similarity == -1)
        if total_edge_count == 0:
            continue
        total_cluster_cnt += 1
        purity += similar_edge_count/total_edge_count

    return purity/total_cluster_cnt
