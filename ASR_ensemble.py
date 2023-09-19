import kenlm
import argparse

def compare_strings_ignore_digits(str1, str2):
    # Remove all digits from both strings
    str1_digits = ''.join(char for char in str1 if  char.isdigit())
    str2_digits = ''.join(char for char in str2 if  char.isdigit())

    # Compare the modified strings
    return str1_digits == str2_digits


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-main', '--main_predict', type=str, required = True)
    args.add_argument('-sup', '--support_predict', type=str, required = True)
    args.add_argument('-lm', '--lm_file', type=str, required = True, help='Path to LM')
    args = args.parse_args()
    path = args.lm_file
    lm = kenlm.LanguageModel(path)

    predictions_file1 = args.main_predict
    predictions_file2 = args.support_predict

    with open(predictions_file1, 'r', encoding='utf-8') as input_file:
        lines1 = input_file.readlines()
        
    with open(predictions_file2, 'r', encoding='utf-8') as input_file:
        lines2 = input_file.readlines()
        
    save = 'ensemble_trans.txt'

    with open(save, 'w', encoding='utf-8') as file:
        for i in range(len(lines1)):
            line1 = lines1[i]
            line2 = lines2[i]
            first_space_index = line1.find(" ")
            path = line1[:first_space_index]
            sentence1 = line1[first_space_index + 1:]
            first_space_index = line2.find(" ")
            sentence2= line2[first_space_index + 1:]
            final_sen = sentence1
            if lm.score(sentence1) + 2 <= lm.score(sentence2):
                final_sen = sentence2
            file.write(path+' '+final_sen)