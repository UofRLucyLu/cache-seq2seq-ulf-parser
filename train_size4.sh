#!/bin/bash
#SBATCH -J hard_s --partition=gpu --gres=gpu:1 --time=5-00:00:00 --output=train.out.size4 --error=train.err.size4
#SBATCH --mem=30GB
#SBATCH --reservation=xpeng3-may2018


module load graphviz

for cache_size in 4 5 6 8; do
    CONFIG_FILE=./jamr_config/config_cache${cache_size}.json
    python NP2P_trainer.py --config_path ${CONFIG_FILE}
done
# CONFIG_FILE=./config_files/config_uniform4.json
# python NP2P_trainer.py --config_path ${CONFIG_FILE}
