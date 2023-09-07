### Train
1. Prepare your dataset
    - To put your dataset in correct format run:
        ```cmd
        python prepare_train_data.py -w [Path to wav data directory] -j [Path to jsonline train file]
        ```
    - Example :
        ```cmd
        python prepare_train_data.py -w SLU_data/train_data/Train/ -j SLU_data/train.jsonl
        ```
3. Run
    - Start training from scratch:
        ```cmd
        python train.py -c config.toml
        ```

<a name = "inference" ></a>
### Inference

1. Transcribe a audio file. 
```cmd
python inference.py -f [Path to your wav file] -m [Path to model.tar]

# output example:
>>> transcript: Hello World 
```

2. Transcribe a list of audio files. 
```cmd
python inference.py -f [Path to your list of wav file] -m [Path to model.tar]
```

    
- Example:
```cmd
python inference.py -f test_file_list.txt -m saved/ASR/checkpoints/best_model.tar
```


This code is base on https://github.com/khanld/ASR-Wav2vec-Finetune 
