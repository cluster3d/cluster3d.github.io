import argparse
import time
from tqdm import tqdm
import torch
import sys
from Dataloader_img_new import * 
from autoencoder_model import *
from torch.utils.tensorboard import SummaryWriter


parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', default="/data2/ABC2/data_img_all/mvcnn_30k/mvcnn-input-pic", required=False, help='Training data root.')
# parser.add_argument('--test_dir', default="/home/yfx/ABC2/onelabel_onelayer_classification/data_img/mvcnn-input-pic", required=False, help='Test data root.')
parser.add_argument('--batchSize', type=int, default=60, help='Batch size.')
parser.add_argument('--epochs', type=int, default=100, help='Number of epochs to train.')
parser.add_argument('--lr', type=float, default=1e-4, help='Learning rate, default=0.0001.')
parser.add_argument('--device', default='cuda:0', help='GPU number, default=0.')
parser.add_argument('--outf', default='/data2/ABC2/log_0208', help='Folder to output log.')
parser.add_argument('--workers', type=int, default=8, help='number of workers used for each Dataloader')
args = parser.parse_args()


def train_process(train_data, model):
    train_loss = 0.
    num_train = 0
    model.train()
    for idx, data in enumerate(tqdm(train_data)):
        optimizer.zero_grad()
        # img_all = data[0] # Bx240x240x3 
        img_all = data.permute(0, 3, 1, 2)
        # ===================forward=====================
        img_all = img_all.float()
        encoded, decoded = model(img_all.cuda()) #encoded: Bx512x15x15; decoded: Bx3x240x240
        # import pdb;pdb.set_trace()
        loss = criterion(decoded.cuda(), img_all.cuda())
        # ===================backward====================
        loss.backward()
        optimizer.step()
        num_train += 1
    # ===================log========================
    train_loss += loss.data

    return train_loss/num_train


train_data = ABC2Dataset_img(args.train_dir)
# test_data = ABC2Dataset_img(args.test_dir)

train_data = torch.utils.data.DataLoader(train_data, batch_size=args.batchSize, shuffle=False)
# test_data = torch.utils.data.DataLoader(test_data, batch_size=args.batchSize, shuffle=False)

model = AutoEncoder_VGG(4).cuda()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)


d=args.outf
tensorboard_save = os.path.join(log_path, str(args.lr))
writer=SummaryWriter(tensorboard_save)

if os.path.exists(log_path)==False:
    os.makedirs(log_path)
parameter_save_path = log_path+"/"+"ae_clustering"+"_Lr_"+str(args.lr)
if os.path.exists(parameter_save_path)==False:
    os.makedirs(parameter_save_path)

# file=open(log_path+"/"+"_Lr_"+str(args.lr)+".txt","w")


for e in range(args.epochs):
    
    start_time = time.time()
    print('###################')
    print('Epoch:', e)
    print('###################')

    train_loss = train_process(train_data, model)

    secs = int(time.time() - start_time)
    mins = secs / 60
    secs = secs % 60

    print('train loss:', train_loss )
    if e % 10 == 0:
        # model_save_path = os.path.join(parameter_save_path+"/"+str(e)+".pth")
        torch.save(model.state_dict(), parameter_save_path + "/" + str(e)+".pth")
    writer.add_scalar('train_loss', train_loss, global_step=e)
writer.close()
    






#     print('epoch [{}/{}], loss:{:.4f}'
#           .format(epoch+1, num_epochs, total_loss))
#     if epoch % 10 == 0:
#         pic = to_img(output.cpu().data)
#         save_image(pic, './dc_img/image_{}.png'.format(epoch))

# torch.save(model.state_dict(), './conv_autoencoder.pth')