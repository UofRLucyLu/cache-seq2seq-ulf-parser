#!/bin/bash

# Exit on failure, since this is a pipeline...
set -e

#SBATCH -J hard_s --partition=gpu --gres=gpu:1 --time=1-00:00:00 --output=decode.cache --error=decode.err_cache
#SBATCH --mem=10GB

# Packages.
module load cuda/8.0
module load cudnn/8.0
module load python/2.7.12
module load tensorflow/1.4.1

# First split up the ULF data into sentences and ULFs.
DATA_SEG="example" # train, dev, test, or example
CACHE_SIZE=2
SET_NAME="5-14"
ULF_VER="${SET_NAME}-${DATA_SEG}"
ULF_DATA=ulfdata/${ULF_VER}
ORACLE_DIR=ulfdata/oracle/${ULF_VER}_cache${CACHE_SIZE}

model_prefix=./logs_cache_size${CACHE_SIZE}_${ULF_VER}/NP2P.base_separate

# The line below is already completed by ulf-pipline.sh
python3 ./oracle/oracle.py --data_dir ${ULF_DATA}/conll --output_dir ${ORACLE_DIR} --cache_size ${CACHE_SIZE} --decode --ulf

python3 NP2P_beam_decoder.py --model_prefix ${model_prefix} \
        --in_path ${ORACLE_DIR} \
        --out_path decode_results/ulf/decode_cache_size${CACHE_SIZE}_${ULF_VER}_instance.amr \
        --mode beam_decode \
        --decode True \
        --cache_size ${CACHE_SIZE} \
        --ulf
  
