#!/bin/bash
#SBATCH -J hard_s --partition=gpu --gres=gpu:1 --time=5-00:00:00 --output=train.out.size6 --error=train.err.size6
#SBATCH --mem=45GB
#SBATCH --reservation=xpeng3-may2018


module load graphviz

CONFIG_FILE=./config_files/config_cache6.json
python NP2P_trainer.py --config_path ${CONFIG_FILE}

CONFIG_FILE=./config_files/config_uniform6.json
python NP2P_trainer.py --config_path ${CONFIG_FILE}
