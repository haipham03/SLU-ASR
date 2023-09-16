### Training
1. Prepare your dataset
    - To put your dataset in correct format and process it run: 
        ```
        bash prepare_train_data.sh [Path to wav data directory] [Path to jsonline train file]
        ```
    - Example :
        ```cmd
        bash prepare_train_data.sh SLU_data/train_data/Train/  SLU_data/train.jsonl
        ```
    - The processed data will be store in `txt_data/process_train.txt`
2. Run
    - Start training from scratch:
        ```cmd
        python train.py -c config.toml
        ```
    - Change the number of workers, epochs, batch size, vv in `config.toml`

<a name = "inference" ></a>
### Inference
```
bash inference.sh [Path to your wav test file lists] [Path to model.tar] [Path to LM model]
```

    
- Example:
```
bash inference.sh data/public_test/ saved/ASR/checkpoints/best_model.tar your_3gram.binary
```

- Then the final transcript be in `process_trans_file.txt`
