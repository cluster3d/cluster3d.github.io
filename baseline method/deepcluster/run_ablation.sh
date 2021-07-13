#!/bin/bash


array=(32 64 128 256 512 1024 2000)

for n in "${array[@]}"
do
    if [[ $n -gt 1 ]];
    then
        CUDA_VISIBLE_DEVICES=2 python3 main.py --nmb_cluster $n 
    fi
done