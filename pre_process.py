import pandas as pd
import argparse
import os

if __name__ == '__main__':
    
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--filepath', type=str, default = 'txt_data/train.txt',
                      help='Path to train file')
    args.add_argument('-s', '--output', type=str, default = None,
                      help='Output processed file')
    args = args.parse_args()
    # file_path = './train_data/aug_train.txt'
    file_path  = args.filepath
    

    df = pd.read_csv(file_path, delimiter = '|')
    
    if args.output is not None :
        save = args.output
    else :
        base_filename, file_extension = os.path.splitext(os.path.basename(file_path))
        new_base_filename = 'process_' + base_filename
        save = os.path.join(os.path.dirname(file_path), new_base_filename + file_extension)

    vietnamese_numbers = {
        '10': 'mười ',
        '11': 'mười một ',
        '12': 'mười hai ',
        '13': 'mười ba ',
        '14': 'mười bốn ',
        '15': 'mười năm ',
        '16': 'mười sáu ',
        '17': 'mười bảy ',
        '18': 'mười tám ',
        '19': 'mười chín ',
        '20': 'hai mươi',
        '30': 'ba mươi',
        '40': 'bốn mươi',
        '50': 'năm mươi',
        '60': 'sáu mươi',
        '70': 'bảy mươi',
        '80': 'tám mươi',
        '90': 'chín mươi',
        '0': 'không ',
        '1': 'một ',
        '2': 'hai ',
        '3': 'ba ',
        '4': 'bốn ',
        '5': 'năm ',
        '6': 'sáu ',
        '7': 'bảy ',
        '8': 'tám ',
        '9': 'chín '
    }


    with open(save, 'w', encoding='utf-8') as file:
        i = 0
        file.write('path|transcript|duration'+'\n')
        for index, row in df.iterrows():
            path = row['path']
            transcript = row['transcript']
            duration = str(row['duration'])
            # print(path,'----',transcript,'---',duration)
            have_number = False
            for key,value in vietnamese_numbers.items():
                if key in transcript:
                    have_number = True
                transcript = transcript.replace(key, value)
            transcript = transcript.strip()

            # Split the string into words and join them with a single space
            transcript = ' '.join(transcript.split())
            # if have_number:
            #     print(path+'|'+transcript+'|'+duration)
            file.write(path+'|'+transcript+'|'+duration+'\n')
            i += 1