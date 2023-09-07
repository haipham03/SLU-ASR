import json
import librosa
from tqdm import tqdm
import pandas as pd
import argparse
import os

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-w', '--test_data_path', type=str, required = True,help='Path to test wav data directory')
    args = args.parse_args()

    # Replace '/path/to/folder' with the actual path of the folder
    folder_path = args.test_data_path

    # Get a list of all file names in the folder
    file_names = os.listdir(folder_path)

    # Write the file names to a text file
    with open('test_file_list.txt', 'w') as file:
        for file_name in file_names:
            file.write( os.path.join(folder_path, file_name) + '\n')