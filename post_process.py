import pandas as pd
import argparse
import os

if __name__ == '__main__':
    
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--filepath', type=str, default = 'transcript_test_file_list.txt',
                      help='Path to transcript file generate by model')
    args = args.parse_args()
    
    file_path = args.filepath

    with open(file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    save = 'process_trans_file.txt'

    vietnamese_numbers = {
        '11': 'mười một',
        '12': 'mười hai',
        '13': 'mười ba',
        '14': 'mười bốn',
        '15': 'mười năm',
        '16': 'mười sáu',
        '17': 'mười bảy',
        '18': 'mười tám',
        '19': 'mười chín',
        '10': 'mười',
        '20': 'hai mươi',
        '30': 'ba mươi',
        '40': 'bốn mươi',
        '50': 'năm mươi',
        '60': 'sáu mươi',
        '70': 'bảy mươi',
        '80': 'tám mươi',
        '90': 'chín mươi',
        '0': 'không',
        '1': 'một',
        '2': 'hai',
        '3': 'ba',
        '4': 'bốn',
        '5': 'năm',
        '6': 'sáu',
        '7': 'bảy',
        '8': 'tám',
        '9': 'chín'
    }

    import re

    with open(save, 'w', encoding='utf-8') as file:
        for line in lines[:]:
            first_space_index = line.find(" ")
            path = line[:first_space_index]
            sentence = line[first_space_index + 1:]
            for key,value in vietnamese_numbers.items():
                sentence = sentence.replace(value, key)
            sentence = sentence.replace(' phần trăm', '%')
            pattern = r'(\d) (\d) (\d)'
            sentence = re.sub(pattern, r'\2 \3', sentence)
            pattern = r'(\d) (\d)'
            sentence = re.sub(pattern, r'\1\2', sentence)
            word = sentence.split()
            sentence = ' '.join(word)
            res = ''
            for id in range(len(sentence)):
                v = sentence[id]
                if v != '0':
                    res += v
                    continue
                if id != 0 and sentence[id-1].isdigit():
                    res += v
                    continue
                if id +1 < len(sentence) and sentence[id+1] == '%':
                    res +=v
                    continue
                if id+5 <= len(sentence) and sentence[id+2:id+5] == 'giờ':
                    res +=v
                    continue
                res += 'không'
            file.write(path+' '+res+'\n')