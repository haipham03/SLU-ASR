### Train
1. Prepare your dataset
    - To put your dataset in correct format run:
        ```
        python prepare_train_data.py -w [Path to wav data directory] -j [Path to jsonline train file]
        ```
    - Example :
        ```cmd
        python prepare_train_data.py -w SLU_data/train_data/Train/ -j SLU_data/train.jsonl
        ```
    - The correct data format will be store in `txt_data/train.txt`
    - To pre process data run:
        ```
        python pre_process.py -f [Path to correct data format txt file]
        ```
    - Example:
        ```cmd
        python pre_process.py -f txt_data/train.txt
        ```
    - The processed data will be store in `txt_data/process_train.txt`
2. Run
    - Start training from scratch:
        ```cmd
        python train.py -c config.toml
        ```

<a name = "inference" ></a>
### Inference

1. Transcribe a audio file. 
```
python inference.py -f [Path to your wav file] -m [Path to model.tar] -lm [Path to LM model]

# output example:
>>> transcript: Hello World 
```

2. Transcribe a list of audio files. 
```
python inference.py -f [Path to your list of wav file] -m [Path to model.tar] -lm [Path to LM model]
```

    
- Example:
```
python inference.py -f test_file_list.txt -m saved/ASR/checkpoints/best_model.tar -lm 3ngram_scratch.binary
```

- The output will be in `transcript_test_file_list.txt`

- To get the final output, run this the post processing file:
```
python post_process.py
```
- Then the final transcript be in `process_trans_file.txt`
