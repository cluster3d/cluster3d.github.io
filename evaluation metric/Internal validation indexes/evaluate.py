#!/usr/bin/env python
# coding: utf-8

# In[6]:


from utils.io import load_file
from sklearn import metrics
from validclust import dunn
import numpy as np


# In[3]:


def silhouette_score(distance_matrix, labels):
    return metrics.silhouette_score(distance_matrix, labels, metric="precomputed")


def dunn_index(distance_matrix, labels):
    return dunn(distance_matrix, labels)



# In[ ]:


# def delta_fast(ck, cl, distance_matrix):
#     values = distance_matrix[np.where(ck)][:, np.where(cl)]
#     values = values[np.nonzero(values)]

#     return np.min(values)


# def big_delta_fast(ci, distance_matrix):
#     values = distance_matrix[np.where(ci)][:, np.where(ci)]
#     # values = values[np.nonzero(values)]

#     return np.max(values)


# def dunn_index(distance_matrix, labels):
#     # Inter-cluster distance
#     ks = np.sort(np.unique(labels))

#     deltas = np.ones([len(ks), len(ks)], dtype=int) * np.iinfo(int).max
#     big_deltas = np.zeros([len(ks), 1])

#     l_range = list(range(0, len(ks)))

#     for k in l_range:
#         for l in (l_range[0:k] + l_range[k + 1:]):
#             deltas[k, l] = delta_fast((labels == ks[k]), (labels == ks[l]), distance_matrix)

#         big_deltas[k] = big_delta_fast((labels == ks[k]), distance_matrix)

#     di = np.min(deltas) / np.max(big_deltas)
#     return di




# def davies_bouldin_index(distance_matrix, labels):
#     # Intra-cluster distance
#     ks = np.sort(np.unique(labels))
#     num_k = len(ks)
#     delta_invs = np.ones([num_k, num_k], dtype=int) * np.iinfo(int).max
#     big_deltas = np.zeros([num_k, 1])

#     l_range = list(range(num_k))

#     for k in l_range:
#         for l in (l_range[0:k] + l_range[k + 1:]):
#             delta_invs[k, l] = 1 / delta_fast((labels == ks[k]), (labels == ks[l]), distance_matrix)

#         big_deltas[k] = big_delta_fast((labels == ks[k]), distance_matrix)

#     dbi = 0
#     ind = np.ones((num_k,), bool)
#     for i in l_range:
#         ind[i] = False
#         dbi += np.max((big_deltas[ind] + big_deltas[i]) * delta_invs[i, ind])
#         ind[i] = True

#     dbi /= num_k
#     return dbi


# In[ ]:


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


# In[ ]:


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

# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:
