This code is adapted from the original implementation of Deep Embedded Clustering (DEC) algorithm. The following readme has details linking the original implementation as well as how to run the models for the Cluster3d dataset. The license from the original implementation has been included in the folder.

PyTorch implementation of a version of the Deep Embedded Clustering (DEC) algorithm. Compatible with PyTorch 1.0.0 and Python 3.6 or 3.7 with or without CUDA.

Paper: "Unsupervised Deep Embedding for Clustering Analysis" of Junyuan Xie, Ross Girshick, Ali Farhadi (<https://arxiv.org/abs/1511.06335>).

Original code that this folder is adapted from: https://github.com/vlukiyanov/pt-dec

## Usage

This is distributed as a Python package `ptdec` and can be installed with `python setup.py install` after installing `ptsdae` from https://github.com/vlukiyanov/pt-sdae. The PyTorch `nn.Module` class representing the DEC is `DEC` in `ptdec.dec`, while the `train` function from `ptdec.model` is used to train DEC.

The example using the Cluster3d dataset can be found and run here: https://github.com/cluster3d/cluster3d.github.io/blob/main/baseline%20method/pt-dec/examples/abc2/abc2.py