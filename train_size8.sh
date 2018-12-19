#!/bin/bash
#SBATCH -J hard_s --partition=gpu --gres=gpu:1 --time=5-00:00:00 --output=train.out.size8 --error=train.err.size8
#SBATCH --mem=45GB
#SBATCH --reservation=xpeng3-may2018


module load graphviz

CONFIG_FILE=./jamr_config/config8.json
#./config_files/config_uniform5.json
python NP2P_trainer.py --config_path ${CONFIG_FILE}

# CONFIG_FILE=./config_files/config_uniform8.json
# python NP2P_trainer.py --config_path ${CONFIG_FILE}
