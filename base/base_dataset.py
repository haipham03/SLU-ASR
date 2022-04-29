import pandas as pd
import sys
import re
import librosa
import numpy as np
from pandarallel import pandarallel

# For testing 
sys.path.append('..')

from sklearn.model_selection import train_test_split
from utils.feature import load_wav
from tqdm import tqdm
from torch.utils.data import Dataset
from dataloader.dataset import Dataset as InstanceDataset
from vietnam_number import n2w



class BaseDataset(Dataset):
    def __init__(self, rank, dist, path, sr, delimiter, min_duration = -np.inf, max_duration = np.inf, preload_data = False, val_size = None, transform = None, nb_workers = 4):
        self.rank = rank
        self.dist = dist
        self.val_size = val_size
        self.sr = sr
        self.transform = transform
        self.preload_data = preload_data
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.df = self.load_data(path, delimiter)
        pandarallel.initialize(progress_bar=True, nb_workers = nb_workers)

        if min_duration != -np.inf or max_duration != np.inf:
            if self.rank == 0 and 'duration' not in self.df.columns:
                print("*****Generate duration column*****")
                self.df['duration'] = self.df['path'].parallel_apply(lambda filename: librosa.get_duration(filename=filename))
                self.df.to_csv(path, index = False, sep = delimiter)
            self.dist.barrier()
            self.df = self.load_data(path, delimiter)
            if self.rank == 0:
                print("*****Filter out invalid audio*****")
            mask = (self.df['duration'] <= self.max_duration) & (self.df['duration'] >= self.min_duration)
            self.df = self.df[mask]
        self.df['transcript'] = self.df['transcript'].apply(self.remove_special_characters)
        
        if self.val_size is not None:
            assert val_size > 0 and val_size < 1, f"val_size should be greater than 0 and smaller than 1, but found {self.val_size}"
            self.train_df, self.test_df = self.split()
        else:
            self.train_df = self.df
    


    def has_numbers(self, text):
        return any(char.isdigit() for char in text)
        
    def remove_special_characters(self, transcript):
        chars_to_ignore_regex = '[^\ a-z0-9A-Z_àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]'
        transcript = re.sub(chars_to_ignore_regex, '', transcript).lower()
        transcript = transcript.split(' ')
        transcript = ' '.join(n2w(text) if text.isnumeric() else '' if self.has_numbers(text) else text for text in transcript)
        return transcript

    def get_vocab_dict(self):
        # Read https://huggingface.co/blog/fine-tune-wav2vec2-english for more information
        all_text = " ".join(list(self.df["transcript"]))
        vocab_list = list(set(all_text))
        vocab_list.sort()
        vocab_dict = {v: k for k, v in enumerate(vocab_list)}

        vocab_dict["|"] = vocab_dict[" "]
        del vocab_dict[" "]
        vocab_dict["[UNK]"] = len(vocab_dict)
        vocab_dict["[PAD]"] = len(vocab_dict)
        return vocab_dict

    def preload_dataset(self, paths, sr):
        wavs = []
        print("Preloading {} data".format(self.mode))
        for path in tqdm(paths, total = len(paths)):
            wav = load_wav(path, sr)
            wavs += [wav]
        return wavs

    def load_data(self, path, delimiter):
        df = pd.read_csv(path, delimiter = delimiter)
        return df

    def split(self):
        return train_test_split(self.df, test_size=self.val_size)

    def get_data(self, mode = 'train'):
        if mode == 'train':
            if self.preload_data:
                if self.rank == 0:
                    print(f"Preloading {len(self.train_df)} data")
                self.train_df['wav'] = self.train_df['path'].parallel_apply(lambda filepath: load_wav(filepath, sr = self.sr))
            train_ds = InstanceDataset(self.train_df, self.sr, self.preload_data, self.transform)
            return train_ds
        else:
            assert self.val_size is not None, f"val_size is not provided, cannot fetch test dataset"
            if self.preload_data:
                if self.rank == 0:
                    print(f"Preloading {len(self.test_df)} data")
                self.test_df['wav'] = self.test_df['path'].parallel_apply(lambda filepath: load_wav(filepath, sr = self.sr))
            test_ds = InstanceDataset(self.test_df, self.sr, self.preload_data, transform = None)
            return test_ds


if __name__ == '__main__':
    ds = BaseDataset(
        path = '/content/drive/MyDrive/ASR Finetune/dataset/vivos/test.csv', 
        sr = 16000, 
        preload_data = False, 
        val_size = None, 
        transform = None)
    
    vocab_dict = ds.get_vocab_dict()
    for k, v in vocab_dict.items():
        print(f'{k} - {v}')