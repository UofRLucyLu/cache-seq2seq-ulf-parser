# ULF-Cache-Seq2seq

This is a Cache Transition Parser for ULF parsing based on the code for the cache transition parser for AMR by Xiaochang Peng.
Large chunks of this code is simply in the state it was when I copied it from the AMR parser, so it won't work or be appropriate
for ULFs.

## File Organization

## BlueHive commands that need to be run before running the parser training.

```
module load cuda/8.0 cudnn/8.0 python/2.7.12
module load tensorflow/1.4.1
module load java
```

If the model is run outside of BlueHive (e.g. to deploy in a task), make sure you get the right version of Python and tensorflow to run it.

