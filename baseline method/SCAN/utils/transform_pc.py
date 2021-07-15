import numpy as np
import torch
class Normalize(object):
    def __init__(self):
        pass

    def __call__(self, batch_data):
        batch_pc, model_ID = batch_data['image'], batch_data['target']
        if len(batch_pc.shape)==2:
            N, C = batch_pc.shape
            normal_data = np.zeros((N, C))
            data = batch_pc
            normal_data = (data - torch.min(data, axis=0)[0])/(torch.max(data, axis=0)[0] + 1e-16 - torch.min(data, axis=0)[0])
            return {'image':normal_data, 'target':model_ID}
        else:
            B, N, C = batch_pc.shape
            normal_data = np.zeros((B, N, C))
            for b in range(B):
                data = batch_pc[b]
                normal_data[b] = (data - torch.min(data, axis=0)[0])/(torch.max(data, axis=0)[0] + 1e-16 - torch.min(data, axis=0)[0])
            return {'image':normal_data, 'target':model_ID}


class ShufflePoints(object):
    def __init__(self):
        pass

    def __call__(self, batch_data):
        # assumes data is in the form 
        # Batch size x point x 3

        batch_pc, model_ID = batch_data['image'], batch_data['target']
        if len(batch_pc.shape)==2:
            idx = np.arange(batch_pc.shape[0])
            np.random.shuffle(idx)
            return {'image': batch_pc[idx,:], 'target': model_ID}  
            
        else:
            idx = np.arange(batch_pc.shape[1])
            np.random.shuffle(idx)
            return {'image': batch_pc[:,idx,:], 'target': model_ID}  

class Rotate(object):
    def __init__(self):
        pass
    def __call__(self, batch_data):
        """ Randomly rotate the point clouds to augument the dataset
            rotation is per shape based along up direction
            Input:
              BxNx3 array, original batch of point clouds
            Return:
              BxNx3 array, rotated batch of point clouds
        """
        batch_pc, model_ID = batch_data['image'], batch_data['target']
        if len(batch_pc.shape)==2:
            rotated_data = np.zeros(batch_pc.shape, dtype=np.float32)
            rotation_angle = np.random.uniform() * 2 * np.pi
            cosval = np.cos(rotation_angle)
            sinval = np.sin(rotation_angle)
            rotation_matrix = np.array([[cosval, 0, sinval],
                                        [0, 1, 0],
                                        [-sinval, 0, cosval]])
            shape_pc = batch_pc
            rotated_data = np.dot(shape_pc.reshape((-1, 3)), rotation_matrix)
        else:
            rotated_data = np.zeros(batch_pc.shape, dtype=np.float32)
            for k in range(batch_pc.shape[0]):
                rotation_angle = np.random.uniform() * 2 * np.pi
                cosval = np.cos(rotation_angle)
                sinval = np.sin(rotation_angle)
                rotation_matrix = np.array([[cosval, 0, sinval],
                                            [0, 1, 0],
                                            [-sinval, 0, cosval]])
                shape_pc = batch_pc[k, ...]
                rotated_data[k, ...] = np.dot(shape_pc.reshape((-1, 3)), rotation_matrix)
        return {'image': rotated_data, 'target': model_ID}  


class RotateZ(object):
    def __init__(self):
        pass
    def __call__(self, batch_data):
        batch_pc, model_ID = batch_data['image'], batch_data['target']
        if len(batch_pc.shape)==2:
            rotated_data = np.zeros(batch_pc.shape, dtype=np.float32)
            rotation_angle = np.random.uniform() * 2 * np.pi
            cosval = np.cos(rotation_angle)
            sinval = np.sin(rotation_angle)
            rotation_matrix = np.array([[cosval, sinval, 0],
                                        [-sinval, cosval, 0],
                                        [0, 0, 1]])
            shape_pc = batch_pc
            rotated_data = np.dot(shape_pc, rotation_matrix)
        else:
            rotated_data = provider.rotate_point_cloud_z(batch_pc)
        return {'image': rotated_data, 'target': model_ID}


class RotatePerturbPC(object):
    def __init__(self):
        pass
    def __call__(self, batch_data, angle_sigma=0.06, angle_clip=0.18):
        batch_pc, model_ID = batch_data['image'], batch_data['target']
        if len(batch_pc.shape)==2:
            rotated_data = np.zeros(batch_pc.shape, dtype=np.float32)
            angles = np.clip(angle_sigma*np.random.randn(3), -angle_clip, angle_clip)
            Rx = np.array([[1,0,0],
                           [0,np.cos(angles[0]),-np.sin(angles[0])],
                           [0,np.sin(angles[0]),np.cos(angles[0])]])
            Ry = np.array([[np.cos(angles[1]),0,np.sin(angles[1])],
                           [0,1,0],
                           [-np.sin(angles[1]),0,np.cos(angles[1])]])
            Rz = np.array([[np.cos(angles[2]),-np.sin(angles[2]),0],
                           [np.sin(angles[2]),np.cos(angles[2]),0],
                           [0,0,1]])
            R = np.dot(Rz, np.dot(Ry,Rx))
            shape_pc = batch_pc[...]
            rotated_data[...] = np.dot(shape_pc, R)            
        else:
            rotated_data = provider.rotate_perturbation_point_cloud(batch_pc)
        return {'image': rotated_data, 'target': model_ID}


class Jitter(object):
    def __init__(self):
        pass
    def __call__(self, batch_data, sigma=0.01, clip=0.05):  
        batch_pc, model_ID = batch_data['image'], batch_data['target']
        
        if (len(batch_pc.shape))==2:
            N, C = batch_pc.shape
            assert(clip > 0)
            jittered_data = np.clip(sigma * np.random.randn(N, C), -1*clip, clip)
            jittered_data += batch_pc
        else:
            jittered_data = provider.jitter_point_cloud(batch_pc)
        return {'image': jittered_data, 'target': model_ID}

class Shift(object):
    def __init__(self):
        pass
    def __call__(self, batch_data, shift_range=0.1):
        batch_pc, model_ID = batch_data['image'], batch_data['target']
        
        if (len(batch_pc.shape))==2:        
            N, C = batch_pc.shape
            shifts = np.random.uniform(-shift_range, shift_range, (3))
            batch_pc[:,:] += shifts[:]
            aug =batch_pc
        else:
            aug = provider.shift_point_cloud(batch_pc)
        return {'image': aug, 'target': model_ID}


class RandomScale(object):
    def __init__(self):
        pass
    def __call__(self, batch_data, scale_low=0.8, scale_high=1.25):     
        batch_pc, model_ID = batch_data['image'], batch_data['target']
        
        if (len(batch_pc.shape))==2:                
            N, C = batch_pc.shape
            scales = np.random.uniform(scale_low, scale_high)
            batch_pc[:,:] *= scales
            aug = batch_pc   
        else:
            aug = provider.random_scale_point_cloud(batch_pc)
        return {'image': aug, 'target': model_ID}


# class RandomPointDropout(object):
#     def __init__(self):
#         pass
#     def __call__(self, batch_data, max_dropout_ratio=0.875): 
#         batch_pc, model_ID = batch_data['image'], batch_data['target']
        
#         if len(batch_pc.shape)==2:
#             dropout_ratio =  np.random.random()*max_dropout_ratio # 0~0.875
#             drop_idx = np.where(np.random.random((batch_pc.shape[1]))<=dropout_ratio)[0]
#             if len(drop_idx)>0:
#                 batch_pc[drop_idx,:] = batch_pc[0,:] # set to the first point
#             aug = batch_pc
#         else:
#             aug = provider.random_point_dropout(batch_pc)
#         return {'image': aug, 'target': model_ID}
        
    

class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, batch_data):

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
        points, model_ID = batch_data['image'], batch_data['target']
        points = torch.from_numpy(points).transpose(1,0).contiguous().type(torch.FloatTensor)

        out = {'image': points, 'target': model_ID}
        return out        
