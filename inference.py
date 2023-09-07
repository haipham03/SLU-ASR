import librosa
import torch
import os
import argparse

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from tqdm import tqdm

from transformers.file_utils import cached_path, hf_bucket_url
import os, zipfile
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import soundfile as sf
import torch
from pyctcdecode import Alphabet, BeamSearchDecoderCTC, LanguageModel
import kenlm
from torch_audiomentations import PeakNormalization

def get_decoder_ngram_model(tokenizer, ngram_lm_path):
    vocab_dict = tokenizer.get_vocab()
    sort_vocab = sorted((value, key) for (key, value) in vocab_dict.items())
    vocab = [x[1] for x in sort_vocab][:-2]
    vocab_list = vocab
    # convert ctc blank character representation
    vocab_list[tokenizer.pad_token_id] = ""
    # replace special characters
    vocab_list[tokenizer.unk_token_id] = ""
    # vocab_list[tokenizer.bos_token_id] = ""
    # vocab_list[tokenizer.eos_token_id] = ""
    # convert space character representation
    vocab_list[tokenizer.word_delimiter_token_id] = " "
    # specify ctc blank char index, since conventially it is the last entry of the logit matrix
    alphabet = Alphabet.build_alphabet(vocab_list, ctc_token_idx = 109)
    lm_model = kenlm.Model(ngram_lm_path)
    decoder = BeamSearchDecoderCTC(alphabet,
                                   language_model=LanguageModel(lm_model))
    return decoder

def normalize(waveform):
    apply_augmentation = PeakNormalization()
    waveform = waveform.reshape((1,1,waveform.shape[0]))
    waveform_tensor = torch.tensor(waveform)
    normalized_waveform_tensor = apply_augmentation(waveform_tensor, sample_rate=16000)
    normalized_waveform = normalized_waveform_tensor.numpy()
    normalized_waveform = normalized_waveform.reshape(normalized_waveform.shape[2])
    return normalized_waveform


class Inferencer:
    def __init__(self, device, huggingface_folder, model_path, lm_path) -> None:
        self.device = device
        self.processor = Wav2Vec2Processor.from_pretrained(huggingface_folder)
        self.model = Wav2Vec2ForCTC.from_pretrained(huggingface_folder).to(self.device)
        if model_path is not None:
            self.preload_model(model_path)
        cache_dir = './cache/'
        processor = Wav2Vec2Processor.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h", cache_dir=cache_dir)
        if lm_path is not None:
            self.ngram_lm_model = get_decoder_ngram_model(processor.tokenizer, lm_path)
        else:
            model = Wav2Vec2ForCTC.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h", cache_dir=cache_dir)
            lm_file = hf_bucket_url("nguyenvulebinh/wav2vec2-base-vietnamese-250h", filename='vi_lm_4grams.bin.zip')
            lm_file = cached_path(lm_file,cache_dir=cache_dir)
            with zipfile.ZipFile(lm_file, 'r') as zip_ref:
                zip_ref.extractall(cache_dir)
            lm_file = cache_dir + 'vi_lm_4grams.bin'
            self.ngram_lm_model = get_decoder_ngram_model(processor.tokenizer, lm_file)


    def preload_model(self, model_path) -> None:
        """
       Preload model parameters (in "*.tar" format) at the start of experiment.
        Args:
            model_path: The file path of the *.tar file
        """
        assert os.path.exists(model_path), f"The file {model_path} is not exist. please check path."
        checkpoint = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(checkpoint["model"], strict = True)
        print(f"Model preloaded successfully from {model_path}.")


 #   def transcribe(self, wav) -> str:
 #       input_values = self.processor(wav, sampling_rate=16000, return_tensors="pt").input_values
 #       logits = self.model(input_values.to(self.device)).logits
 #       pred_ids = torch.argmax(logits, dim=-1)
 #       pred_transcript = self.processor.batch_decode(pred_ids)[0]
 #       return pred_transcript

    def transcribe(self, wav) -> str:
        input_values = self.processor(wav, sampling_rate=16000, return_tensors="pt").input_values
        logits = self.model(input_values.to(self.device)).logits
        pred_ids = torch.argmax(logits, dim=-1)
        beam_search_output = [
                self.ngram_lm_model.decode(
                    logit,
                    beam_width=500
                )
                for logit in logits.cpu().detach().numpy()
        ]
        pred_transcript = self.processor.batch_decode(pred_ids)[0]
        if "độ c" in pred_transcript:
            print(pred_transcript,'-------------' ,beam_search_output[0].replace("độ","độ c "))
        return beam_search_output[0].replace("độ","độ c ")


    def run(self, test_filepath):
        filename = test_filepath.split('/')[-1].split('.')[0]
        filetype = test_filepath.split('.')[1]
        if filetype == 'txt':
            f = open(test_filepath, 'r')
            lines = f.read().splitlines()
            f.close()

            f = open(test_filepath.replace(filename, 'transcript_'+filename), 'w+')
            for line in tqdm(lines):
                wav, _ = librosa.load(line, sr = 16000)
                wav = normalize(wav)
                transcript = self.transcribe(wav)
                f.write(line + ' ' + transcript + '\n')
            f.close()

        else:
            wav, _ = librosa.load(test_filepath, sr = 16000)
            wav = normalize(wav)
            print(f"transcript: {self.transcribe(wav)}")


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='ASR INFERENCE ARGS')
    args.add_argument('-f', '--test_filepath', type=str, required = True,
                      help='It can be either the path to your audio file (.wav, .mp3) or a text file (.txt) containing a list of audio file paths.')
    args.add_argument('-s', '--huggingface_folder', type=str, default = 'huggingface-hub',
                      help='The folder where you stored the huggingface files. Check the <local_dir> argument of [huggingface.args] in config.toml. Default value: "huggingface-hub".')
    args.add_argument('-m', '--model_path', type=str, default = None,
                      help='Path to the model (.tar file) in saved/<project_name>/checkpoints. If not provided, default uses the pytorch_model.bin in the <HUGGINGFACE_FOLDER>')
    args.add_argument('-d', '--device_id', type=int, default = 0,
                      help='The device you want to test your model on if CUDA is available. Otherwise, CPU is used. Default value: 0')
    args.add_argument('-lm', '--lm_file', type=str, default = None,
                      help='Path to LM')                  
    args = args.parse_args()
    
    device = f"cuda:{args.device_id}" if torch.cuda.is_available() else "cpu"

    inferencer = Inferencer(
        device = device, 
        huggingface_folder = args.huggingface_folder, 
        model_path = args.model_path,
        lm_path = args.lm_file)

    inferencer.run(args.test_filepath)

