import os
import csv
from tqdm import tqdm
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("result_dir", type=str)
parser.add_argument("result_matrix_path", type=str)
parser.add_argument("data_dir", type=str)
parser.add_argument("check_integrity", type=bool, default=True)
parser.add_argument("check_excessive_result", type=bool, default=True)

args = parser.parse_args()
result_dir = args.result_dir
result_matrix_path = args.result_matrix_path
data_dir = args.data_dir
check_integrity = args.check_integrity
check_excessive_result = args.check_excessive_result
del args

# 1. Check Data Integrity

result_list = sorted(os.listdir(result_dir), key=lambda name: int(name.split('_')[-2]))
data_list = os.listdir(data_dir)
start_end = {}
for full_name in result_list:
    split = full_name.split('_')
    try:
        start = int(split[-2])
        end = int(split[-1].split('.')[0])
    except:
        print(full_name)
        break
    if start in start_end:
        print("duplicated results! for start", start, "already have end", start_end[start], "but now also have", end)
        raise Exception("fix this before moving on!")
    start_end[start] = end

if check_integrity:
    def find_next_in_dict(start_end, start):
        keys = np.array(list(start_end.keys()))
        after_start = keys[keys > start]
        return min(after_start)

    current_start = 0
    num_res = len(result_list)
    error_list = [""]
    print_step = 50
    for result_count in range(num_res):
        try:
            current_end = start_end[current_start]
        except:
            try:
                current_end = find_next_in_dict(start_end, current_start)
            except:
                current_end = current_start
                break
            full_name = "chamfer_distance_{}_{}.csv".format(current_start, current_end)
            print("missing the result", full_name)
            if error_list[-1] != full_name: error_list.append(full_name)
            current_start = current_end
            if result_count % print_step == 0:
                print("result", result_count, "finished.")
            continue
        full_name = "chamfer_distance_{}_{}.csv".format(current_start, current_end)
        row_count = 0
        with open(os.path.join(result_dir, full_name), 'r', newline='') as current_result:
            for row_idx, row in enumerate(csv.reader(current_result)):
                try:
                    assert(len(row) == current_start + row_idx + 1)
                except:
                    print("number of columns in row", row_idx, "of file", full_name, "should be", current_start + row_idx + 1, \
                         "but get", len(row), "instead.")
                    if error_list[-1] != full_name: error_list.append(full_name)
                row_count += 1
        try:
            assert(row_count == current_end - current_start)
        except:
            print("number of rows of file", full_name, "should be", current_end - current_start, \
                  "but get", row_count, "instead.")
            if error_list[-1] != full_name: error_list.append(full_name)
        current_start = current_end
        if result_count % print_step == 0:
            print("result", result_count, "finished.")

    error_list = error_list[1:]
    try:
        assert(current_end == len(data_list))
    except:
        print("expecting", len(data_list), "objects but get", current_end, "objects")
        full_name = "chamfer_distance_{}_{}.csv".format(current_end, len(data_list))
        error_list.append(full_name)
    print("number of results:", num_res)
    print("numer of errors:", len(error_list))
    if len(error_list) > 0:
        print("error list:")
        print(error_list)




if check_excessive_result:
    starts = []
    current_start = 0
    while current_start in start_end:
        starts.append(current_start)
        current_start = start_end[current_start]
    if len(starts) != len(result_list):
        assert(len(starts) < len(result_list))
        print("exist", len(result_list)-len(starts), "extra files")
        excessive_result = []
        for result_name in result_list:
            if int(result_name.split('_')[-2]) not in starts:
                excessive_result.append(result_name)
                os.system("mv {} ~/trash".format(os.path.join(result_dir, result_name)))
        print("removed excessive results:", excessive_result)
        raise Exception("fix this before moving on!")
    else:
        print("no excessive result.")


class MergeResults(object):
    def __init__(self, data_list, result_list, result_dir):
        # check result_list
        previous_end = result_list[0].split('_')[-1].split('.')[0]
        for i in range(1, len(result_list)):
            split = result_list[i].split('_')
            start = split[-2]
            try:
                assert (start == previous_end)
            except:
                raise Exception(result_list[i - 1], result_list[i])
            previous_end = split[-1].split('.')[0]
        self.result_list = result_list
        self.result_dir = result_dir

        self.data_list = np.asarray(data_list)
        self.n = len(data_list)
        self.unsortedidx_sortedidx = np.zeros(self.n, dtype=int)
        for sortedidx, unsortedidx in enumerate(np.argsort(self.data_list)):
            self.unsortedidx_sortedidx[unsortedidx] = sortedidx

        self.data = np.zeros(self.n * (self.n - 1) // 2)
        self.ii = np.zeros(self.n * (self.n - 1) // 2, dtype=int)
        self.jj = np.zeros(self.n * (self.n - 1) // 2, dtype=int)
        #         self.data = [0.] * (self.n * (self.n-1) // 2)
        #         self.ii = [0] * (self.n * (self.n-1) // 2)
        #         self.jj = [0] * (self.n * (self.n-1) // 2)
        self.dist_count = 0
        self.row_count = 0
        self.sorted_data_list = sorted(data_list)

    def add_distance(self, idx1, idx2, distance):
        assert (idx1 != idx2)
        self.data[self.dist_count] = distance
        if idx1 < idx2:
            self.ii[self.dist_count] = idx2
            self.jj[self.dist_count] = idx1
        else:
            self.ii[self.dist_count] = idx1
            self.jj[self.dist_count] = idx2
        self.dist_count += 1

    def merge_results(self):
        for result_name in tqdm(self.result_list):
            with open(os.path.join(self.result_dir, result_name), 'r', newline='') as result:
                for row_idx, row in enumerate(csv.reader(result)):
                    distance_enum = enumerate(row, start=-1)
                    row_name = distance_enum.__next__()[1]
                    sorted_row_idx = self.unsortedidx_sortedidx[self.row_count]
                    try:
                        assert (row_name == self.sorted_data_list[sorted_row_idx])
                    except:
                        raise Exception("in" + result_name + "row" + row_idx + "row name should be" + row_name + \
                                        "but get" + self.sorted_data_list[sorted_row_idx])

                    for column_idx, distance in distance_enum:
                        sorted_column_idx = self.unsortedidx_sortedidx[column_idx]
                        self.add_distance(sorted_column_idx, sorted_row_idx, distance)
                    self.row_count += 1
                self.row_start = row_idx + 1


merger = MergeResults(data_list, result_list, result_dir)
merger.unsortedidx_sortedidx[22967]
temp = np.array(data_list)
merger = MergeResults(data_list, result_list, result_dir)
merger.merge_results()
del data_list
del result_list
del start_end
import scipy.sparse as sp
distance_matrix = sp.coo_matrix((merger.data, (merger.ii, merger.jj)))
del merger
distance_matrix = distance_matrix.tocsr()
sp.save_npz(result_matrix_path, distance_matrix)
