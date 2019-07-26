#!/bin/bash
#SBATCH --partition=gpu --gres=gpu:1 --time=2:00:00 --output=eval.out --error=eval.err
#SBATCH --mem=10GB

# Packages.
module load java
module load cuda/8.0 cudnn/8.0 python/2.7.12
module load tensorflow/1.4.1

start=`date +%s`
cache_size=4
model_prefix=./logs_cache_size${cache_size}_hard_ulf/NP2P.base_separate
python NP2P_evaluater.py --model_prefix ${model_prefix} \
        --in_path ulfdata/oracle/12-15-dev_cache${cache_size} \
        --decode True \
        --cache_size ${cache_size} \
        --ulf

end=`date +%s`
runtime=$((end-start))
echo $runtime
