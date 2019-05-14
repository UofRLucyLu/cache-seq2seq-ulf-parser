#!/bin/bash
#SBATCH -J hard_s --partition=gpu --gres=gpu:1 --time=1-00:00:00 --output=decode.cache --error=decode.err_cache
#SBATCH --mem=10GB

# Packages.
module load java
module load cuda/8.0 cudnn/8.0 python/2.7.12
module load tensorflow/1.4.1
#conda activate ~/anaconda2/envs/test

# The line below is already completed by ulf-pipline.sh
#python ./oracle/oracle.py --data_dir ./ulfdata/12-15-dev --output_dir ./ulfdata/oracle/12-15-${split}-cache${cache_size} --cache_size 4 --decode --ulf

cache_size=6
split="test"
beam_size=10
model_prefix=./logs_cache_size${cache_size}_hard_ulf/NP2P.base_separate
#model_prefix=./logs_decode_dev/NP2P.base_separate
#python soft_beam_decoder.py --model_prefix ${model_prefix} \
python NP2P_beam_decoder.py --model_prefix ${model_prefix} \
        --in_path ./ulfdata/oracle/12-15-${split}_cache${cache_size} \
        --out_path decode_results/ulf/decode_${split}_hard_${cache_size}_instance.amr \
        --mode beam_decode \
        --decode True \
        --cache_size ${cache_size} \
        --ulf

        #--out_path decode_results/ulf/hard_cache${cache_size}_beam${beam_size}.amr \
#        --in_path ./data/ulfdata-xc \

  
  
  
# GK: Below is the original AMR cache transition parser decode.sh commented out for reference.  
#start=`date +%s`
#declare -a beam_size=(5 10 20 1) 
#for size in ${beam_size[@]}; do
#    for cache_size in 5 4 6 8; do
#    #python NP2P_beam_decoder.py --model_prefix logs/NP2P.$1 \
#    #        --in_path dev_uniform \
#    #        --out_path logs/hard_dev_beam${size}.$1\.tok \
#    #        --mode beam_decode \
#    #        --decode True \
#    #        --cache_size 5
#
#    # python NP2P_beam_decoder.py --model_prefix logs/NP2P.$1 \
#    #         --in_path test_uniform \
#    #         --out_path logs/hard_test_beam${size}.$1\.tok \
#    #         --mode beam_decode \
#    #         --decode True \
#    #         --cache_size 5
#    model_prefix=./logs_cache_size${cache_size}_separate/NP2P.base_separate
#    python NP2P_beam_decoder.py --model_prefix ${model_prefix} \
#            --in_path ./jamr_data/dev_cache${cache_size}_decode \
#            --out_path decode_results/dev/hard_cache${cache_size}_beam${size}.amr \
#            --mode beam_decode \
#            --decode True \
#            --cache_size ${cache_size}
#done
#done
#
#end=`date +%s`
#runtime=$((end-start))
#echo $runtime
