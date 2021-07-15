#!/bin/bash
array=(32 64 128 256 512 1024 2000)

for n in "${array[@]}"
do
    if [[ $n -gt 1 ]];
    then
        CUDA_VISIBLE_DEVICES=1 python scan.py --config_exp configs/scan/scan_abc2.yml --config_env configs/env.yml --num_classes $n
    fi
done
