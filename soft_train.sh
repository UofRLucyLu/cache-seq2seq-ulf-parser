#!/bin/bash
#SBATCH -J soft_s --partition=gpu --gres=gpu:1 --time=2-00:00:00 --output=soft_train.out --error=soft_train.err
#SBATCH --mem=35GB


module load graphviz

for cache_size in 4 6; do
    CONFIG_FILE=./soft_config/config_cache${cache_size}.json
    python soft_NP2P_trainer.py --config_path ${CONFIG_FILE}
done
# python soft_NP2P_trainer.py --config_path config.json
