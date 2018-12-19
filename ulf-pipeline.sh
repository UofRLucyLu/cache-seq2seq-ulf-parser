#!/bin/bash

# Exit on failure, since this is a pipeline...
set -e

#SBATCH -J oracle_run --time=2:00:00 --output=oracle.out --error=oracle.err
#SBATCH --mem=20GB
#SBATCH -c 4

# Packages.
module load java
module load cuda/8.0 cudnn/8.0 python/2.7.12
module load tensorflow/1.4.1
#conda activate ~/anaconda2/envs/test

# First split up the ULF data into sentences and ULFs.
DATA_SEG="dev"
ULF_VER="12-15-${DATA_SEG}"
ULF_DATA=ulfdata/${ULF_VER}

# This script generates the basic files from the SQL output tsv files.
#python ulf-preproc/preproc-ulf.py ulf-preproc/config/${ULF_VER}-config.json
#cp ulf-preproc/result/${ULF_VER}-preproc/* ${ULF_DATA}

# Move the original data to the processing dir.
#cp initial-ulf-data/${ULF_VER} ulfdata/

# Use the stanford parser to get POS and NER tags and tokenize and lemmatize
PARSER_DIR=./tools/stanford-parser-full-2017-06-09
CORENLP_VER=stanford-corenlp-full-2018-10-05
# the sentences.
TAGGER_DIR=./tools
# Args: [corenlp] [output dir] [input/output directory] [input file]
#${TAGGER_DIR}/stanford-preprocess.sh ${CORENLP_VER}/ ${ULF_DATA} ${ULF_DATA} raw

# NB: Here you'll need to use Lisp scripts in cycle to generate the ULF-AMR files
#     and alignments.  TODO: actually the alignments can be done here since it uses
#     just python.
# Assume for now that ${ULF_DATA}/amr contains that AMR formatted ULF formulas.
#python data_processing/ulf_align.py ${ULF_DATA} ${ULF_DATA}/amr ${ULF_DATA}/alignment.amr xiaochang t 

# Generate the CoNLL
# Categorize data
#CONLL_GEN=data/ulfdata
#CONLL_GEN=data/${ULF_VER}
CONLL_GEN=${ULF_DATA}/conll
# TODO: rename the task since I'm not actually categorizing ULF at all...
#python data_processing/prepareTokens.py --task categorize --data_dir ${ULF_DATA} --use_lemma --run_dir ${CONLL_GEN} --stats_dir ${CONLL_GEN}/stats --conll_file ${CONLL_GEN}/amr_conll --table_dir ${ULF_DATA}/tables
cp ${ULF_DATA}/dep ${CONLL_GEN}/dep

CACHE_SIZE=4
ORACLE_DIR=ulfdata/oracle/${ULF_VER}_cache${CACHE_SIZE}
#python ./oracle/oracle.py --data_dir ${CONLL_GEN} --output_dir ${ORACLE_DIR} --cache_size ${CACHE_SIZE} --ulf

# Generate decoding...
python ./oracle/oracle.py --data_dir ${CONLL_GEN} --output_dir ${ORACLE_DIR} --cache_size ${CACHE_SIZE} --ulf --decode
cp ${ORACLE_DIR}/oracle_decode.json ${ORACLE_DIR}/decode.json


# Training...
#SBATCH -J hard_s --partition=gpu --gres=gpu:1 --time=5-00:00:00 --output=train.out_separate --error=train.err_separate
#SBATCH --mem=35GB
#SBATCH -c 1
#SBATCH --reservation=xpeng3-may2018

module load graphviz

CONFIG_FILE=./config_files/config_ulf_cache${CACHE_SIZE}.json
#./config_files/config_uniform5.json
# TODO: use hard attention
#python soft_NP2P_trainer.py --config_path ${CONFIG_FILE}
#python NP2P_trainer.py --config_path ${CONFIG_FILE}

























# Use stanford parser to get tokenized sentences.
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

#python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache4 --cache_size 4
#python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache4 --cache_size 4
#python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache5 --cache_size 5
#python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache5 --cache_size 5
#python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache6 --cache_size 6
#python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache6 --cache_size 6
#python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache8 --cache_size 8
#python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache8 --cache_size 8

# python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache4_arc50 --cache_size 4
# python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache4_arc50 --cache_size 4
# python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache5_arc50 --cache_size 5
# python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache5_arc50 --cache_size 5
# python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache6_arc50 --cache_size 6
# python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache6_arc50 --cache_size 6
# python ./oracle/oracle.py --data_dir ./jamr_data/training --output_dir ./jamr_data/train_oracle_cache8_arc50 --cache_size 8
# python ./oracle/oracle.py --data_dir ./jamr_data/dev --output_dir ./jamr_data/dev_oracle_cache8_arc50 --cache_size 8
