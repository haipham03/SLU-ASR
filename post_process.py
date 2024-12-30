import pandas as pd
import argparse
import os
import re

def has_consecutive_duplicates(text):
    # Use regular expressions to find consecutive duplicate words
    pattern = r'\b(\w+)\s+\1\b'
    return bool(re.search(pattern, text))


if __name__ == '__main__':
    
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--filepath', type=str, default = 'transcript_test_file_list.txt',
                      help='Path to transcript file generate by model')
    args.add_argument('-s', '--save_name', type=str, default = 'process_trans_file.txt',
                      help='save name')
    args = args.parse_args()
    
    file_path = args.filepath

    with open(file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    save = args.save_name

    vietnamese_numbers = {
        ' 1 1 ': 'mười một',
        ' 1 2 ': 'mười hai',
        ' 1 3 ': 'mười ba',
        ' 1 4 ': 'mười bốn',
        ' 1 5 ': 'mười năm',
        ' 1 6 ': 'mười sáu',
        ' 1 7 ': 'mười bảy',
        ' 1 8 ': 'mười tám',
        ' 1 9 ': 'mười chín',
        ' 1 0 ': 'mười',
        ' 2 0 ': 'hai mươi',
        ' 3 0 ': 'ba mươi',
        ' 4 0 ': 'bốn mươi',
        ' 5 0 ': 'năm mươi',
        ' 6 0 ': 'sáu mươi',
        ' 7 0 ': 'bảy mươi',
        ' 8 0 ': 'tám mươi',
        ' 9 0 ': 'chín mươi',
        ' 0 ': 'không',
        ' 1 ': 'một',
        ' 2 ': 'hai',
        ' 3 ': 'ba ',
        ' 4 ': 'bốn',
        ' 5 ': 'năm',
        ' 6 ': 'sáu',
        ' 7 ': 'bảy',
        ' 8 ': 'tám',
        ' 9 ': 'chín '
    }

    with open(save, 'w', encoding='utf-8') as file:
        for line in lines[:]:
            first_space_index = line.find(" ")
            path = line[:first_space_index]
            sentence = line[first_space_index + 1:]
            for key,value in vietnamese_numbers.items():
                sentence = sentence.replace(value, key)
            sentence = sentence.replace('chín\n', '9\n')
            sentence = sentence.replace('ba\n', '3\n')
            sentence = ' '.join(sentence.split())
            sentence = sentence.replace(' phần trăm', '% ')
            pattern = r'(\d) (\d) (\d) (\d)'
            sentence = re.sub(pattern, r'\3 \4', sentence)
            pattern = r'(\d) (\d) (\d)'
            sentence = re.sub(pattern, r'\2 \3', sentence)
            pattern = r'(\d) (\d)'
            sentence = re.sub(pattern, r'\1\2', sentence)
            word = sentence.split()
            sentence = ' '.join(word)

            # pattern = r'(\d)\s+giờ\s+(\w+)\s+(\d)'
            # result = re.sub(pattern, r'\1 giờ kém \3', sentence)

            # sentence = result

            res = ''
            for id in range(len(sentence)):
                v = sentence[id]
                if v == '1' :
                    if sentence[id+2:id+5] == 'lúc' and id+5<len(sentence):
                        res += 'một'
                        continue 
                    if sentence[id+2:id+5] == 'số' and id+5<len(sentence):
                        res += 'một'
                        continue 
                    if sentence[id+2:id+6] == 'chút' and id+6<len(sentence):
                        res += 'một'
                        continue 
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
            if has_consecutive_duplicates(res):
                pattern = r'\b(\w+)\s+\1\b'
                res = re.sub(pattern, r'\1', res)
            file.write(path+' '+res+'\n')
            
    with open(save, 'r') as file:
        lines = file.readlines()

    # Convert the lines to lowercase and then sort them by the lowercase WAV file names in ascending order
    sorted_lines = sorted(lines, key=lambda line: line.split('/')[-1].lower())

    # Write the sorted lines to a new text file
    with open(save, 'w') as file:
        file.writelines(sorted_lines)