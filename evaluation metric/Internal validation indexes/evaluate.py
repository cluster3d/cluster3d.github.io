from utils.io import load_file
from sklearn import metrics
from validclust import dunn
import numpy as np

def silhouette_score(distance_matrix, labels):
    return metrics.silhouette_score(distance_matrix, labels, metric="precomputed")


def dunn_index(distance_matrix, labels):
    return dunn(distance_matrix, labels)

def intra_cluster_purity_cluster_normalize(similarity_matrix, cluster_result, verbose=False, check_symmetric=False):
    purity = 0
    num_cluster = len(cluster_result)
    if check_symmetric:
        try:
            assert ((similarity_matrix == similarity_matrix.T).all())
        except:
            print(np.where(similarity_matrix != similarity_matrix.T))
            raise Exception("similarity matrix not symmetric.")
    for current_cluster in tqdm(cluster_result):
        num_obj = len(current_cluster)
        if num_obj < 2:
            num_cluster -= 1
            continue
        cluster_similarity = similarity_matrix[current_cluster, :][:, current_cluster]

        similar_count = np.count_nonzero(cluster_similarity == 1)
        total_count = similar_count + np.count_nonzero(cluster_similarity == -1)
        if total_count == 0:
            num_cluster -= 1
            continue
        purity += similar_count / total_count
        if verbose:
            #             print("current cluster:", current_cluster)
            print("purity:", similar_count / total_count, "similar_count:", similar_count, "dissimilar count:",
                  np.count_nonzero(cluster_similarity == -1))

    if verbose:
        print("total purity", purity, "number of non-trivial clusters:", num_cluster)
    purity /= num_cluster
    return purity


def intra_cluster_purity_edge_normalize(similarity_matrix, cluster_result, verbose=False, check_symmetric=False):
    purity = 0
    num_cluster = len(cluster_result)
    if check_symmetric:
        try:
            assert ((similarity_matrix == similarity_matrix.T).all())
        except:
            print(np.where(similarity_matrix != similarity_matrix.T))
            raise Exception("similarity matrix not symmetric.")
    for current_cluster in tqdm(cluster_result):
        num_obj = len(current_cluster)
        if num_obj < 2:
            num_cluster -= 1
            continue
        cluster_similarity = similarity_matrix[current_cluster, :][:, current_cluster]

        similar_count = np.count_nonzero(cluster_similarity == 1)
        total_count = similar_count + np.count_nonzero(cluster_similarity == -1)
        if total_count == 0:
            num_cluster -= 1
            continue
        purity += similar_count / total_count
        if verbose:
            # print("current cluster:", current_cluster)
            print("purity:", similar_count / total_count, "similar_count:", similar_count, "dissimilar count:",
                  np.count_nonzero(cluster_similarity == -1))

    if verbose:
        print("total purity", purity, "number of non-trivial clusters:", num_cluster)
    purity /= num_cluster
    return purity


def evaluate(evaluation_method,
             distance_matrix=None,
             labels=None,
             similarity_matrix=None,
             cluster_list=None,
             verbose=False,
             check_symmetric=False):
    score = None
    # purity
    if evaluation_method == 'intra_cluster_purity_cluster_normalize':
        score = intra_cluster_purity_cluster_normalize(similarity_matrix, cluster_list, verbose, check_symmetric)
    # distance
    elif evaluation_method == 'silhouette_score':
        score = silhouette_score(distance_matrix, labels)
    elif evaluation_method == 'dunn_index':
        score = dunn_index(distance_matrix, labels)
    elif evaluation_method == 'davies_bouldin_index':
        score = davies_bouldin_index(distance_matrix, labels)

    return score