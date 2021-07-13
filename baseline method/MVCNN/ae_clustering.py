import argparse
import time
from tqdm import tqdm
import torch
import sys
import pandas as pd 
from Dataloader_img_new import * 
from autoencoder_model import *
from torch.utils.tensorboard import SummaryWriter
from sklearn.cluster import KMeans
import numpy as np


parser = argparse.ArgumentParser()
# parser.add_argument('--test_dir', default="/data2/ABC2/test_img", required=False, help='Testing data root.')
parser.add_argument('--test_dir', default="/data2/ABC2/new_clustering_img/mvcnn_all/mvcnn-input-pic", required=False, help='Test data root.')
parser.add_argument('--para_dir', default="/data2/ABC2/log_clustering_old/70.pth", required=False, help='saved parameter root.')
# batchsize should satisfy: models*(img num in each model)  %  batchsize == 0 
parser.add_argument('--batchSize', type=int, default=96, help='Batch size.')
parser.add_argument('--epochs', type=int, default=100, help='Number of epochs to train.')
parser.add_argument('--lr', type=float, default=1e-4, help='Learning rate, default=0.0001.')
parser.add_argument('--device', default='cuda:2', help='GPU number, default=0.')
parser.add_argument('--outf', default='/data2/ABC2/log_0220/', help='Folder to output log.')
parser.add_argument('--workers', type=int, default=16, help='number of workers used for each Dataloader')
args = parser.parse_args()


def feature_concatenate(encoded_part):

    ave_pool = torch.nn.AvgPool2d((11, 11), stride=(5, 5))
    feature_12_img = ave_pool(encoded_part).reshape(-1,512) # 512*1
    return feature_12_img


def test_process(test_data, model, batchsize):

    test_loss = 0.
    num_test = 0
    model.eval()
    num_folder = int(batchsize/12)
    all_feature = []
    list_folder = []
    with torch.no_grad():
        for idx, data in enumerate(tqdm(test_data)):
            img_all = data[0] # Bx240x240x3
            img_all = img_all.reshape(img_all.shape[0], 3, img_all.shape[1], img_all.shape[2])
            # ===================forward=====================
            img_all = img_all.float()
            encoded, decoded = model(img_all.to(args.device)) #encoded: Bx512x15x15; decoded: Bx3x240x240
            # ===================every ave pooling to convert each feature (512x15x15) -> 512x1=====================
            feature_12_img = feature_concatenate(encoded)
            # ===================concatenate features for each 12 images, then use ave pooling to =====================
            feature_each_image = torch.zeros(num_folder, 12, 512) # (B/12)x12x512
            for i in range(num_folder):
                feature_each_image[i, :, :] = feature_12_img[12*i:12*(i+1), :]
                list_folder.append('%08d'%(int(data[1][12*i])))

            # ===================return feature with its folder name=====================
            # out_feature = torch.cat((aaa,bbb,ccc,ddd,eee), 0) #5x512
            out_feature = torch.mean(feature_each_image, 1) #5x512
            out_feature_np = out_feature.cpu().detach().numpy() 
            all_feature.append(out_feature_np)

            # if(idx>60):
            #     break
            
        return all_feature, list_folder


test_data = ABC2Dataset_img(args.test_dir)
test_data = torch.utils.data.DataLoader(test_data, batch_size=args.batchSize, shuffle=False)
model = AutoEncoder_VGG(4)
model.load_state_dict(torch.load(args.para_dir, map_location='cpu'))
model.to(args.device)
model.eval()

log_path=args.outf


if os.path.exists(log_path)==False:
    os.makedirs(log_path)
parameter_save_path = log_path+"/"+"ae_clustering"+"_Lr_"+str(args.lr)
if os.path.exists(parameter_save_path)==False:
    os.makedirs(parameter_save_path)

list_folder_all = []


tmp_out_feature, list_folder = test_process(test_data, model, args.batchSize) # size: tmp_out_features: list_folder/8, since each feature has batch/12 model features

divided_num = int(args.batchSize / 12)
tmp = divided_num*len(tmp_out_feature)
all_features = np.zeros((int(tmp), 512))
for i in range(len(tmp_out_feature)):
    all_features[int(divided_num)*i:int(divided_num)*(i+1), :] = tmp_out_feature[i]

for i in range(0, len(list_folder)):
    list_folder[i] = int(list_folder[i])
list_folder_int = torch.IntTensor(list_folder).reshape(len(list_folder),-1)



# ID_and_features = torch.cat((list_folder_int, torch.tensor(all_features)),1)
# torch.save(ID_and_features, '/data2/ABC2/feature_img_tsne.pt')


kmeans = KMeans(n_clusters=1000, random_state=0).fit(all_features)
kmeans.labels_
list_folder_arr = np.array(list_folder)

final = np.concatenate((list_folder_arr.reshape(list_folder_arr.shape[0], 1), kmeans.labels_.reshape(kmeans.labels_.shape[0], 1)), axis=1)

# np.savetxt('clustering_all_20k.txt', final)
df = pd.DataFrame(columns=['ID', 'which_cluster'])
for i in range(final.shape[0]):
    df.loc[-1] = [final[i][0], final[i][1]]
    # import pdb;pdb.set_trace()
    df.index = df.index + 1
    df = df.sort_values('ID')

df.to_csv('/data2/ABC2/clustering_all_20k.csv', index=False)




# # #--------------------------------------------------------------------------------------------
# # label = kmeans.labels_
# # # label = np.random.randint(1000,size=1000)
# # from collections import Counter
# # d2 = Counter(label)
# # sorted_x = sorted(d2.items(), key=lambda x: x[1], reverse=False)
# # sort_num = np.array(sorted_x)
# # np.savetxt('clustering_good_bad.txt', sort_num)
# # # import pdb;pdb.set_trace()

# # import numpy as np
# # import matplotlib
# # matplotlib.use('Agg')
# # import matplotlib.pyplot as plt
# # plt.figure(figsize=(15,8))
# # # rects1 = plt.bar(x=sort_num[:,0], height=sort_num[:,1], width=0.4, alpha=0.8, color='red')
# # plt.bar(np.arange(len(sort_num[:,1])), sort_num[:,1])
# # plt.xlabel("cluster")
# # plt.ylabel("number")
# # # plt.show()
# # plt.savefig('clustering_good_bad.jpg')

# # bigger_index = sort_num[:,0][sort_num[:,1]>10]
# # id_list = []
# # for idx in bigger_index:
# #     index = np.arange(final.shape[0])[label==idx]
# #     for i in index:
# #         # print(list_folder[i])
# #         id_list.append(list_folder[i])

# # df = pd.DataFrame(columns=['ID'])
# # for i in range(len(id_list)):
    
# #     df.loc[-1] = [id_list[i]]
# #     df.index = df.index + 1
# #     df = df.sort_values('ID')
    
# # # df.to_csv('/data2/ABC2/clustering_good_bad.csv', index=False)
# # # while(len(bigger_index)):

    