#!/usr/bin/env python
# coding: utf-8

# In[1]:


from iou_constants import data_dir, code_dir, dimension, temp_export_type, binvox_program_path
import trimesh
from trimesh.exchange import binvox
import subprocess
import os
import numpy as np
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("start", type=int)
parser.add_argument("end", type=int)
args = parser.parse_args()
start = args.start
end = args.end
del args

# In[2]:


def remove(file_types):
    if len(file_types) == 0:
        return
    
    for obj_name in tqdm(os.listdir(data_dir)):
        obj_dir = os.path.join(data_dir, obj_name)
        command = ""
        for file_type in file_types:
            command += "rm {}/*.{};".format(obj_dir, file_type)
        os.system(command)
    
# remove([temp_export_type, 'binvox', 'npy'])
remove([])



def temp_binvox(temp_export_path):
    output = subprocess.run('export LD_PRELOAD=/share/apps/local/lib/libGL.so; xvfb-run -d -w 0 {} -d {} {}'.format(binvox_program_path, dimension, temp_export_path),
                            shell=True, capture_output=True)
    try:
        assert(output.returncode == 0 and output.stdout.decode('ascii').split('\n')[-3] == 'done')
#         assert(output.returncode == 0)
    except:
        raise Exception(output.stdout.decode('ascii'))
    
def binvox_npy(name_base, binvox_path, align_center=False):
    with open(binvox_path, 'rb') as fp:
        voxel_grid = np.array(binvox.load_binvox(fp, axis_order='xyz').matrix)
#     if align_center:
#         coordinates = np.where(voxel_grid == 1)
#         new_coordinates = [None] * 3 
#         for i in range(3):
#             min_diff = min(coordinates[i])
#             max_diff = dimension - 1 - max(coordinates[i])
#             new_coordinates[i] = coordinates[i] + (max_diff - min_diff) // 2
#             voxel_grid = np.zeros((dimension, dimension, dimension))
#             voxel_grid[new_coordinates[0], new_coordinates[1], new_coordinates[2]] = 1
    
    np.save(name_base.format('npy'), voxel_grid)
    
def mesh_npy(mesh, type_name, obj_name, obj_dir):
    name_base = os.path.join(obj_dir, '{}_{}.{}'.format(obj_name, type_name, '{}'))
    
    npy_path = name_base.format('npy')
    if not os.path.exists(npy_path):
        binvox_path = name_base.format('binvox')
        if not os.path.exists(binvox_path):
            temp_export_path = name_base.format(temp_export_type)
            if not os.path.exists(temp_export_path):
                with open(temp_export_path, 'wb') as fp:
                    mesh.export(fp, file_type=temp_export_type)
            else:
                print("object", obj_name, "already have", type_name, temp_export_type, "file generated.")
            temp_binvox(temp_export_path)
        else:
            print("object", obj_name, "already have", type_name, "binvox file generated.")
        binvox_npy(name_base, binvox_path, align_center=(type_name=='align_center'))
    else:
        print("object", obj_name, "already have npy file generated.")


# In[4]:


for obj_name in tqdm(os.listdir(data_dir)[start:end]):
    obj_dir = os.path.join(data_dir, obj_name)
    files = os.listdir(obj_dir)
    for file_name in files:
        if 'obj' in file_name:
            obj_path = os.path.join(obj_dir,file_name)
            break
    
    # align center
#     mesh = trimesh.load_mesh(obj_path)
#     mesh_npy(mesh, 'align_center', obj_name, obj_dir)
    
    # min-max normalization
    mesh = trimesh.load_mesh(obj_path)
    [bbox_min, bbox_max] = mesh.bounds
    if (bbox_min == bbox_max).any():
        npy_path = os.path.join(obj_dir, '{}_{}.{}'.format(obj_name, 'normalized', 'npy'))
        if os.path.exists(npy_path):
            print("object", obj_name, "already have npy file generated.")
        else:
            print("object", obj_name, "is depreciated.")
            np.save(npy_path, np.zeros((dimension, dimension, dimension)))
    mesh.vertices = (mesh.vertices - bbox_min) / (bbox_max - bbox_min)
    mesh_npy(mesh, 'normalized', obj_name, obj_dir)




def test():
    import cProfile, pstats, io
    from pstats import SortKey
    pr = cProfile.Profile()
    pr.enable()
    for obj_name in tqdm(os.listdir(data_dir)[166:169]):
        obj_dir = os.path.join(data_dir, obj_name)
        files = os.listdir(obj_dir)
        for file_name in files:
            if 'obj' in file_name:
                obj_path = os.path.join(obj_dir,file_name)
                break
        mesh = trimesh.load_mesh(obj_path)
        # align center
        mesh_npy(mesh, 'align_center', obj_name)

        # min-max normalization
        [bbox_min, bbox_max] = mesh.bounds
        mesh.vertices = (mesh.vertices - bbox_min) / (bbox_max - bbox_min)
        mesh_npy(mesh, 'normalized', obj_name)
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())


