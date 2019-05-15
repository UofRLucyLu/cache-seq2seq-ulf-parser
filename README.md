# ULF-Cache-Seq2seq

This is a Cache Transition Parser for ULF parsing based on the code for the cache transition parser for AMR by Xiaochang Peng.
Large chunks of this code is simply in the state it was when I copied it from the AMR parser, so it won't work or be appropriate
for ULFs.

## File Organization

- `ulf-pipeline.sh` : The main script for preprocessing the inputs (file with sentences with corresponding ULFs) to generate the features, run the oracle, and then train the model.
- `ulf-decode.sh` : Script to decode amr format instances from the raw decoded oracle actions.
- `eval.sh` : Run evaluator. I don't remember exactly what is generated here. I'm pretty sure it only evaluates against the oracle action accuracy.
- `NP2P_*.py` : Various model specific code (in the original version is was distinct from the soft attention version of the code.
- `*_utils.py` : General utility functions in the code.
- `oracle/` : Folder with all the code for the oracle.
- `config_files/` : Configuration files for training.
- `tools/` : External tools used for preprocessing (e.g. Stanford NLP Pipeline).
- `data/vectors.txt`, `data/vectors.txt.st` : Glove word embeddings.

## BlueHive commands that need to be run before running the parser training.

```
module load cuda/8.0 cudnn/8.0 python/2.7.12
module load tensorflow/1.4.1
module load java
```

If the model is run outside of BlueHive (e.g. to deploy in a task), make sure you get the right version of Python and tensorflow to run it.

