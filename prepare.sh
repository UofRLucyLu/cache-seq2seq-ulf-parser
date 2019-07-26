#!/bin/bash
#SBATCH --partition=gpu --gres=gpu:1 --time=2:00:00 --output=eval.out --error=eval.err
#SBATCH --mem=10GB
#SBATCH -c 6

start=`date +%s`
# declare -a beam_size=(5 10 20 1) 
declare -a beam_size=(5) 
for size in ${beam_size[@]}; do
    # for cache_size in 5 4 6; do
    for cache_size in 5; do
    DECODE_FILE=./decode_results/dev/soft_cache${cache_size}_beam${size}.amr
    RESULT_DIR=./decode_results/dev_amr/soft_cache${cache_size}_beam${size}
    ./amr.sh ${DECODE_FILE} ${RESULT_DIR} ./jamr_data/dev/token

    DECODE_FILE=./decode_results/test/soft_cache${cache_size}_beam${size}.amr
    RESULT_DIR=./decode_results/test_amr/soft_cache${cache_size}_beam${size}
    ./amr.sh ${DECODE_FILE} ${RESULT_DIR} ./jamr_data/test/token

done
done

end=`date +%s`
runtime=$((end-start))
echo $runtime
