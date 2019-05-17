#!/bin/bash

# Exit on failure, since this is a pipeline...
set -e

#SBATCH --partition=gpu --gres=gpu:1 --time=2:00:00 --output=eval.out --error=eval.err
#SBATCH --mem=10GB

# Packages.
module load cuda/8.0
module load cudnn/8.0
module load python/2.7.12
module load tensorflow/1.4.1

start=`date +%s`
DATA_SEG="example" # train, dev, test, or example
CACHE_SIZE=2
SET_NAME="5-14"
ULF_VER="${SET_NAME}-${DATA_SEG}"
ORACLE_DIR=ulfdata/oracle/${ULF_VER}_cache${CACHE_SIZE}

model_prefix=./logs_cache_size${CACHE_SIZE}_${ULF_VER}/NP2P.base_separate

python NP2P_evaluator.py --model_prefix ${model_prefix} \
        --in_path ${ORACLE_DIR} \
        --decode True \
        --cache_size ${CACHE_SIZE} \
        --ulf

end=`date +%s`
runtime=$((end-start))
echo $runtime

