#!/usr/bin/bash
result_amr=$1
result_dir=$2
tok_file=$3
mkdir -p ${result_dir}
grep "# tok::" ${result_amr} > ${result_dir}/toks
grep "# sentence-" ${result_amr} > ${result_dir}/idxs
sed -i "s/^# tok:: //" ${result_dir}/toks
sed -i "s/^# sentence-//" ${result_dir}/idxs
python ./data_processing/amr_utils.py ${result_amr} ${tok_file} ${result_dir} ${result_dir}/amr ${result_dir}/output.amr
sed -i "s/([0-9]*)//" ${result_dir}/output.amr
