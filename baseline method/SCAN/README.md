This code is adapted from the original implementation of SCAN: Learning to Classify Images without Labels. The following readme has details linking the original implementation as well as how to run the models for the Cluster3d dataset. The license from the original implementation has been included in the folder.


Paper: [**SCAN: Learning to Classify Images without Labels**](https://arxiv.org/pdf/2005.12320.pdf)


## Installation
The code runs with recent Pytorch versions, e.g. 1.4. 
Assuming [Anaconda](https://docs.anaconda.com/anaconda/install/), the most important packages can be installed as:
```shell
conda install pytorch=1.4.0 torchvision=0.5.0 cudatoolkit=10.0 -c pytorch
conda install matplotlib scipy scikit-learn   # For evaluation and confusion matrix visualization
conda install faiss-gpu                       # For efficient nearest neighbors search 
conda install pyyaml easydict                 # For using config files
conda install termcolor                       # For colored print statements
```
We refer to the `requirements.txt` file for an overview of the packages in the environment we used to produce our results.


### Train model
The configuration files for cluster3d can be found in the `configs/` directory. The training procedure consists of the following steps:
- __STEP 1__: Solve the pretext task i.e. `simclr.py`
- __STEP 2__: Perform the clustering step i.e. `scan.py`
- __STEP 3__: Perform the self-labeling step i.e. `selflabel.py`

For example, run the following commands sequentially to perform the method on Cluster3D:
```shell
python simclr.py --config_env configs/your_env.yml --config_exp configs/pretext/simclr_abc2.yml
python scan.py --config_env configs/your_env.yml --config_exp configs/scan/scan_abc2.yml
python selflabel.py --config_env configs/your_env.yml --config_exp configs/selflabel/selflabel_abc2.yml
```

