#!/bin/bash
#SBATCH --partition=gpu --gres=gpu:1 --time=2:00:00 --output=eval.out --error=eval.err
#SBATCH --mem=10GB


start=`date +%s`
model_prefix=./logs_cache_size5_separate/NP2P.base_separate
python NP2P_evaluater.py --model_prefix ${model_prefix} \
        --in_path jamr_data/dev_oracle_cache5 \
        --decode True \
        --cache_size 5

end=`date +%s`
runtime=$((end-start))
echo $runtime
