This code is based on the original AtlasNet implementation. The following readme has details linking the original AtlasNet implementation as well as how to run the models for the Cluster3d dataset. The license from the original implementation has been included in the folder.


**AtlasNet: A Papier-Mâché Approach to Learning 3D Surface Generation** <br>
Thibault Groueix,  Matthew Fisher, Vladimir G. Kim , Bryan C. Russell, Mathieu Aubry  <br>
In [CVPR, 2018](http://cvpr2018.thecvf.com/).



### Install

This implementation uses Python 3.6, [Pytorch](http://pytorch.org/), [Pymesh](https://github.com/PyMesh/PyMesh), Cuda 10.1. 
```shell
# Copy/Paste the snippet in a terminal
git clone --recurse-submodules https://github.com/ThibaultGROUEIX/AtlasNet.git
cd AtlasNet 

#Dependencies
conda create -n atlasnet python=3.6 --yes
conda activate atlasnet
conda install  pytorch torchvision cudatoolkit=10.1 -c pytorch --yes
pip install --user --requirement  requirements.txt # pip dependencies
```



##### Optional : Compile Chamfer (MIT) + Metro Distance (GPL3 Licence)
```shell
# Copy/Paste the snippet in a terminal
python auxiliary/ChamferDistancePytorch/chamfer3D/setup.py install #MIT
cd auxiliary
```


##### Usage: 
  
Run `train.py` with arguments specified in `auxiliary/argument_parser`.
The dataset loaded is modified to be the Cluster3d dataset in the following files:
- https://github.com/cluster3d/cluster3d.github.io/blob/main/baseline%20method/AtlasNet/dataset/trainer_dataset.py
- https://github.com/cluster3d/cluster3d.github.io/blob/main/baseline%20method/AtlasNet/dataset/dataset_abc2.py

