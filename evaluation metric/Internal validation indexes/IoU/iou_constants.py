import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

name = 'IoU'
data_dir_relative = 'obj_correct_num'
iou_coo_args_dir_relative = 'coo_args'
iou_coo_args_name_start_end = 'iou_coo_args_{}_{}.npz'

dimension = 128
temp_export_type = 'off'
binvox_program_path = 'binvox'
env_name = 'pytorch3d'
npy_types = ['normalized']

data_dir = os.path.join(data_dir, data_dir_relative)
result_dir = os.path.join(result_dir, name)
code_dir = os.path.join(code_dir, name)
output_dir = os.path.join(output_dir, name)

binvox_program_path = os.path.join(code_dir, binvox_program_path)
iou_coo_args_dir = os.path.join(result_dir, iou_coo_args_dir_relative)

num_data = len(os.listdir(data_dir))
