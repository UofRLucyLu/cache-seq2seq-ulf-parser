#!/bin/bash
#SBATCH -J hard_s --partition=gpu --gres=gpu:1 --time=2-00:00:00 --output=train.out.cache_size --error=train.err.cache_size
#SBATCH --mem=20GB

module load graphviz

for cache_size in 8; do
    CONFIG_FILE=./jamr_config/config_cache${cache_size}.json
    python NP2P_trainer.py --config_path ${CONFIG_FILE}
done
# CONFIG_FILE=./config_files/config_uniform4.json
# python NP2P_trainer.py --config_path ${CONFIG_FILE}
