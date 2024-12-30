import json
import librosa
from tqdm import tqdm
import pandas as pd
import argparse
import os

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-tw', '--train_data_path', type=str, required = True,help='Path to train wav data directory')
    args.add_argument('-vw', '--val_data_path', type=str, required = False,help='Path to val wav data directory')
    args.add_argument('-t', '--train_jsonline_path', type=str, required = True,help='Path to jsonline train file')
    args.add_argument('-v', '--val_jsonline_path', type=str, required = False,help='Path to jsonline val file')
    
    args = args.parse_args()

    train_jsonl = args.train_jsonline_path
    train_path = args.train_data_path
    val_jsonl = args.val_jsonline_path
    val_path = args.val_data_path

    # Open the JSONL file for reading
    i = 0
    os.makedirs('txt_data', exist_ok=True)
    with open('txt_data/train.txt', 'w', encoding="utf8") as train_txt:
        with open(train_jsonl, 'r', encoding="utf8") as file:
            for line in tqdm(file):
                # Load each line as a JSON object
                json_object = json.loads(line)
                wav_file = os.path.join(train_path, json_object['file'])
                # server_wav_file = '/data1.local/vinhpt/phh/ASR-Wav2vec-Finetune/data/augmented_data/' + json_object['file']
                sentence = json_object['sentence']
                n_sentence = sentence.replace("%", " phần trăm") 
                duration = librosa.get_duration(filename=wav_file)
                train_line = wav_file + '|' + n_sentence + '|' + str(duration)
                
                if i == 0:
                    train_txt.write("path|transcript|duration" + '\n')
                train_txt.write(train_line + '\n')
                i += 1

    # i = 0
    # with open('txt_data/val.txt', 'w', encoding="utf8") as val_txt:
    #     with open(val_jsonl, 'r', encoding="utf8") as file:
    #         for line in tqdm(file):
    #             # Load each line as a JSON object
    #             json_object = json.loads(line)
    #             wav_file = os.path.join(val_path, json_object['file'])
    #             # server_wav_file = '/data1.local/vinhpt/phh/ASR-Wav2vec-Finetune/data/augmented_data/' + json_object['file']
    #             sentence = json_object['sentence']
    #             n_sentence = sentence.replace("%", " phần trăm") 
    #             val_line =  wav_file + '|' + n_sentence
            
    #             if i == 0:
    #                 val_txt.write("path|transcript" + '\n')
    #             val_txt.write(val_line + '\n')
                
    #             # Example: Accessing specific fields
    #             # field_value = json_object['field_name']
    #             i += 1

