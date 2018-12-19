#!/bin/bash
#SBATCH -J hard_s --partition=gpu --gres=gpu:1 --time=1-00:00:00 --output=decode.cache --error=decode.err_cache
#SBATCH --mem=10GB

start=`date +%s`
declare -a beam_size=(5 10 20 1) 
for size in ${beam_size[@]}; do
    for cache_size in 5 4 6; do
    model_prefix=./logs_cache_size${cache_size}_separate/NP2P.base_separate
    python NP2P_beam_decoder.py --model_prefix ${model_prefix} \
            --in_path ./jamr_data/dev_cache${cache_size}_decode \
            --out_path decode_results/dev/hard_cache${cache_size}_beam${size}.amr \
            --mode beam_decode \
            --decode True \
            --cache_size ${cache_size}
done
done

end=`date +%s`
runtime=$((end-start))
echo $runtime
