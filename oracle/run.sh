#!/bin/bash
DATA_DIR=../data/train_categorized
OUTPUT_DIR=../data/train_oracle
python ./oracle.py --data_dir $DATA_DIR --output_dir $OUTPUT_DIR --cache_size 4
