import kenlm
import json
from tqdm import tqdm
import copy
import argparse

def has_common_substring(str1, str2):
        # Iterate through the first string
        for i in range(len(str1) - 2):
            for j in range(i + 3, len(str1) + 1):
                substring = str1[i:j]
                # Check if the substring exists in the second string
                if substring in str2:
                    return True
        return False

def have_same_3_chars_in_order(str1, str2):
    for i in range(len(str1)-2):
        for j in range(i+1,len(str1)-1):
            for k in range(j+1,len(str1)):
                for ii in range(len(str2)-2):
                    for jj in range(ii+1,len(str2)-1):
                        for kk in range(jj+1,len(str2)):
                            if str1[i] == str2[ii] and str1[j] == str2[jj] and str1[k] == str2[kk]:
                                return True
    return False

if __name__ == '__main__':
    
    args = argparse.ArgumentParser()
    args.add_argument('-j', '--jsonline_path', type=str, required = True,
                      help='Path to jsonline train')
    args.add_argument('-lm', '--lm_file', type=str, required = True, help='Path to LM')
    args.add_argument('-p', '--predict_file', type=str, required = True, help='Path to last ASR predict file')
    args = args.parse_args()
    path = args.lm_file
    jsonl_file = args.jsonline_path
    # path = 'D:/ASR-Wav2vec-Finetune/your_3gram.binary'
    # jsonl_file = 'C:/Users/Admin/Downloads/train.jsonl'
    lm = kenlm.LanguageModel(path)

    word_vectors = {}

    with open(jsonl_file, 'r', encoding="utf8") as file:
        for line in tqdm(file):
            # Load each line as a JSON object
            json_object = json.loads(line)
            sentence = json_object['sentence']
            sentence=sentence.replace("%", " phần trăm").lower()
            sentence=sentence.replace(",","")
            words = sentence.split()
            for i in range(len(words) - 1):
                current_word = copy.deepcopy(words[i])
                next_word = words[i + 1]

                # Create a key for the current word and append the next word to its value
                if current_word.isdigit() : 
                    current_word = "digits"
                    if next_word == "hình":
                        print(sentence)
                if current_word in word_vectors :
                    if next_word not in word_vectors[current_word]:
                        word_vectors[current_word].append(next_word)
                else:
                    word_vectors[current_word] = [next_word]

    # for word, next_words in word_vectors.items():
    #     print(f"{word}: {next_words}")
    print(word_vectors['digits'])
        
    # sentence1 = "máy tính để bàn của khang"
    # print(sentence1, lm.score(sentence1))

    # sentence2 = "máy tính đểa bàn của khang"
    # print(sentence2, lm.score(sentence2))

    predict_file = args.predict_file

    with open(predict_file, 'r', encoding='utf-8') as input_file:
        lines1 = input_file.readlines()
        
    save = 'final_trans.txt'
    with open(save, 'w', encoding='utf-8') as file:
        for i in range(len(lines1)):
            line1 = lines1[i]
            first_space_index = line1.find(" ")
            path = line1[:first_space_index]
            sentence1 = line1[first_space_index + 1:]
            sentence1=sentence1.replace("%", " phần trăm") 
            words = sentence1.split()
            best = lm.score(sentence1)
            replace = sentence1
            for i in range(len(words) - 1):
                current_word = copy.deepcopy(words[i])
                if current_word.isdigit() : 
                    current_word = "digits"
                if current_word not in word_vectors:
                    continue
                next_word = words[i + 1]
                if next_word in word_vectors[current_word]:
                    continue
                for replace_word in word_vectors[current_word]:
                    if have_same_3_chars_in_order(replace_word, next_word):
                        test_sentence = ""
                        for j in range(len(words)):
                            if j == i + 1 :
                                test_sentence += replace_word + " "
                                continue
                            test_sentence += words[j] + " "
                        if lm.score(test_sentence) > best:
                            replace = test_sentence
                            best = lm.score(test_sentence)
            if sentence1 == replace or lm.score(sentence1) + 2.3 >  lm.score(replace):
                sentence1=sentence1.replace(" phần trăm","%")
                file.write(path+' '+sentence1)
                continue
            print(path)
            print(sentence1, lm.score(sentence1))
            print(replace, lm.score(replace))
            replace = replace.replace(" phần trăm", "%")
            file.write(path+' '+replace+'\n')
                    