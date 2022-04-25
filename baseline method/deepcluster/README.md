This code is adapted from the original implementation of Deep Clustering for Unsupervised Learning of Visual Features. The following readme has details linking the original implementation as well as how to run the models for the Cluster3d dataset. The license from the original implementation has been included in the folder.

DeepCluster paper: (https://arxiv.org/abs/1807.05520)

Original implementaton: (https://github.com/facebookresearch/deepcluster)


## Requirements

- a Python installation version 2.7
- the SciPy and scikit-learn packages
- a PyTorch install version 0.1.8 ([pytorch.org](http://pytorch.org))
- CUDA 8.0
- a Faiss install ([Faiss](https://github.com/facebookresearch/faiss))
- The ImageNet dataset (which can be automatically downloaded by recent version of [torchvision](https://pytorch.org/docs/stable/torchvision/datasets.html#imagenet))



## Running the unsupervised training

Unsupervised training can be launched by running:
```
$ python3 main.py --nmb_cluster $n 
```
Please provide the path to the data folder:
```
DIR='/data2/ABC2/data_raw_clustering/pc_correct_num'
```
To train an AlexNet network, specify `ARCH=alexnet` whereas to train a VGG-16 convnet use `ARCH=vgg16`.

You can also specify where you want to save the clustering logs and checkpoints using:
```
EXP=exp
```

During training, models are saved every other n iterations (set using the `--checkpoints` flag), and can be found in for instance in `${EXP}/checkpoints/checkpoint_0.pth.tar`.
A log of the assignments in the clusters at each epoch can be found in the pickle file `${EXP}/clusters`.


Full documentation of the unsupervised training code `main.py`:
```
usage: main.py [-h] [--arch ARCH] [--sobel] [--clustering {Kmeans,PIC}]
               [--nmb_cluster NMB_CLUSTER] [--lr LR] [--wd WD]
               [--reassign REASSIGN] [--workers WORKERS] [--epochs EPOCHS]
               [--start_epoch START_EPOCH] [--batch BATCH]
               [--momentum MOMENTUM] [--resume PATH]
               [--checkpoints CHECKPOINTS] [--seed SEED] [--exp EXP]
               [--verbose]
               DIR

PyTorch Implementation of DeepCluster

positional arguments:
  DIR                   path to dataset

optional arguments:
  -h, --help            show this help message and exit
  --arch ARCH, -a ARCH  CNN architecture (default: alexnet)
  --sobel               Sobel filtering
  --clustering {Kmeans,PIC}
                        clustering algorithm (default: Kmeans)
  --nmb_cluster NMB_CLUSTER, --k NMB_CLUSTER
                        number of cluster for k-means (default: 10000)
  --lr LR               learning rate (default: 0.05)
  --wd WD               weight decay pow (default: -5)
  --reassign REASSIGN   how many epochs of training between two consecutive
                        reassignments of clusters (default: 1)
  --workers WORKERS     number of data loading workers (default: 4)
  --epochs EPOCHS       number of total epochs to run (default: 200)
  --start_epoch START_EPOCH
                        manual epoch number (useful on restarts) (default: 0)
  --batch BATCH         mini-batch size (default: 256)
  --momentum MOMENTUM   momentum (default: 0.9)
  --resume PATH         path to checkpoint (default: None)
  --checkpoints CHECKPOINTS
                        how many iterations between two checkpoints (default:
                        25000)
  --seed SEED           random seed (default: 31)
  --exp EXP             path to exp folder
  --verbose             chatty
```


```
