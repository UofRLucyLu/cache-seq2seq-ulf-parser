#!/bin/bash
#SBATCH -J oracle_run --time=2:00:00 --output=oracle.out --error=oracle.err
#SBATCH --mem=20GB
#SBATCH -c 4

# Use stanford parser to get tokenized sentences.
PARSER_DIR=./tools/stanford-parser-full-2017-06-09
# $PARSER_DIR/lexparser.sh ./data/dev/token dev.tmp > dev.log
# $PARSER_DIR/grammar-structure.sh dev.tmp ./data/dev/dep.conll
# 
# $PARSER_DIR/lexparser.sh ./data/test/token test.tmp > test.log
# $PARSER_DIR/grammar-structure.sh test.tmp ./data/test/dep.conll
 
# $PARSER_DIR/lexparser.sh ./data/train/token train.tmp > train.log
# $PARSER_DIR/grammar-structure.sh train.tmp ./data/train/dep.conll

# Get tokenized form
# python ./depTokens.py ./data/train/dep.conll ./data/train_tokenized
# python ./depTokens.py ./data/dev/dep.conll ./data/dev_tokenized
# python ./depTokens.py ./data/test/dep.conll ./data/test_tokenized

# Get lemmatized tokens.
# python lemmatize_snts.py --data_dir ./data/train_tokenized --lemma_dir ./lemmas 
# python lemmatize_snts.py --data_dir ./data/dev_tokenized --lemma_dir ./lemmas
# python lemmatize_snts.py --data_dir ./data/test_tokenized --lemma_dir ./lemmas

# Realign to the tokenized file.
# python ./prepareTokens.py --task realign --input_file ./data/train/token --token_file ./data/train_tokenized/token --align_file ./data/train/alignment --output ./data/train_tokenized/alignment
# python ./prepareTokens.py --task realign --input_file ./data/dev/token --token_file ./data/dev_tokenized/token --align_file ./data/dev/alignment --output ./data/dev_tokenized/alignment

# Categorize data
# python ./prepareTokens.py --task categorize --data_dir ./data/train_tokenized --use_lemma --run_dir data/train_categorized --stats_dir stats --conll_file data/train_categorized/amr
# python ./prepareTokens.py --task categorize --data_dir ./data/dev_tokenized --use_lemma --run_dir data/dev_categorized --stats_dir stats --conll_file dev.conll

# Rerun the dependency on the categoriezed tokens.
# TOKEN_FILE=./data/train_categorized/token
# TREE_FILE=${TOKEN_FILE}.tree
# CONLL_FILE=./data/train_categorized/dep
# $PARSER_DIR/lexparser.sh $TOKEN_FILE $TREE_FILE > dep.log
# $PARSER_DIR/grammar-structure.sh $TREE_FILE $CONLL_FILE

# TOKEN_FILE=./data/dev_categorized/token
# TREE_FILE=${TOKEN_FILE}.tree
# CONLL_FILE=./data/dev_categorized/dep
# $PARSER_DIR/lexparser.sh $TOKEN_FILE $TREE_FILE > dep.log
# $PARSER_DIR/grammar-structure.sh $TREE_FILE $CONLL_FILE

# Extract the oracle for the training data
# python ./oracle/oracle.py --data_dir ./data/train_categorized --output_dir ./data/train_oracle_size4 --cache_size 4
# python ./oracle/oracle.py --data_dir ./data/train_categorized --output_dir ./data/train_oracle_size5 --cache_size 5
# python ./oracle/oracle.py --data_dir ./data/train_categorized --output_dir ./data/train_oracle_size6 --cache_size 6
# python ./oracle/oracle.py --data_dir ./data/train_categorized --output_dir ./data/train_oracle_size8 --cache_size 8
# python ./oracle/oracle.py --data_dir ./data/dev_categorized --output_dir ./data/dev_oracle_size4 --cache_size 4

# python ./oracle/oracle.py --data_dir ./data/dev_categorized --output_dir ./data/dev_oracle_size5 --cache_size 5
# python ./oracle/oracle.py --data_dir ./data/dev_categorized --output_dir ./data/dev_oracle_size6 --cache_size 6
# python ./oracle/oracle.py --data_dir ./data/dev_categorized --output_dir ./data/dev_oracle_size8 --cache_size 8
python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache4 --cache_size 4
python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache4 --cache_size 4
python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache5 --cache_size 5
python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache5 --cache_size 5
python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache6 --cache_size 6
python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache6 --cache_size 6
python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache8 --cache_size 8
python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache8 --cache_size 8

# python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache4_arc50 --cache_size 4
# python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache4_arc50 --cache_size 4
# python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache5_arc50 --cache_size 5
# python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache5_arc50 --cache_size 5
# python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache6_arc50 --cache_size 6
# python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache6_arc50 --cache_size 6
# python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache8_arc50 --cache_size 8
# python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache8_arc50 --cache_size 8
