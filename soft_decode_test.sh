#!/bin/bash
#SBATCH -J hard_s --partition=gpu --gres=gpu:1 --time=1-00:00:00 --output=soft.test.decode.cache --error=soft.test.decode.err_cache
#SBATCH --mem=10GB

start=`date +%s`
# declare -a beam_size=(5 10) 
declare -a beam_size=(5) 
for size in ${beam_size[@]}; do
    for cache_size in 5 4 6; do
    model_prefix=./soft_cache_size${cache_size}_separate/NP2P.base_separate
    # python ./soft_beam_decoder.py --model_prefix ${model_prefix} \
    #         --in_path ./jamr_data/dev_cache${cache_size}_decode \
    #         --out_path decode_results/dev/soft_cache${cache_size}_beam${size}.amr \
    #         --mode beam_decode \
    #         --decode True \
    #         --cache_size ${cache_size}
    
    model_prefix=./soft_cache_size${cache_size}_separate/NP2P.base_separate
    python ./soft_beam_decoder.py --model_prefix ${model_prefix} \
            --in_path ./jamr_data/test_cache${cache_size}_decode \
            --out_path decode_results/test/soft_cache${cache_size}_beam${size}.amr \
            --mode beam_decode \
            --decode True \
            --cache_size ${cache_size}
done
done

end=`date +%s`
runtime=$((end-start))
echo $runtime
