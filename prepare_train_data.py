import json
import librosa
from tqdm import tqdm
import pandas as pd
import argparse
import os

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-w', '--wav_data_path', type=str, required = True,help='Path to wav data directory')
    args.add_argument('-j', '--jsonline_path', type=str, required = True,help='Path to jsonline train file')
    args = args.parse_args()

    jsonl_file_path = args.jsonline_path
    train_path = args.wav_data_path

    # Open the JSONL file for reading
    i = 0
    os.makedirs('txt_data', exist_ok=True)
    with open('txt_data/train.txt', 'w', encoding="utf8") as train_txt, open('txt_data/test.txt', 'w', encoding="utf8") as test_txt:
        with open(jsonl_file_path, 'r', encoding="utf8") as file:
            for line in tqdm(file):
                # Load each line as a JSON object
                json_object = json.loads(line)
                wav_file = os.path.join(train_path, json_object['file'])
                server_wav_file = '/data1.local/vinhpt/phh/ASR-Wav2vec-Finetune/data/augmented_data/' + json_object['file']
                sentence = json_object['sentence']
                n_sentence = sentence.replace("%", " phần trăm") 
                duration = librosa.get_duration(filename=wav_file)
                train_line = wav_file + '|' + n_sentence + '|' + str(duration)
                test_line =  wav_file + '|' + n_sentence
                
                if i == 0:
                    train_txt.write("path|transcript|duration" + '\n')
                train_txt.write(train_line + '\n')

                if i == 0:
                    test_txt.write("path|transcript" + '\n')
                test_txt.write(test_line + '\n')
                
                # Example: Accessing specific fields
                # field_value = json_object['field_name']
                i += 1

