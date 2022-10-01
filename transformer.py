from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import torch

import soundfile as sf


 
 # load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-lv-60-espeak-cv-ft")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-lv-60-espeak-cv-ft")
     
 # load dummy dataset and read soundfiles
ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")
print(ds[0]["audio"]["array"])
print(ds[0]['text'])
def map_to_array(batch):
    speech_array, _ = sf.read(batch)
    return speech_array
data = map_to_array('test2mono.flac')  
 # tokenize
input_values = processor(data, return_tensors="pt").input_values
 
 # retrieve logits
with torch.no_grad():
    logits = model(input_values).logits
 
 # take argmax and decode
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)
 # => should give ['m ɪ s t ɚ k w ɪ l t ɚ ɹ ɪ z ð ɪ ɐ p ɑː s əl ʌ v ð ə m ɪ d əl k l æ s ᵻ z æ n d w iː ɑːɹ ɡ l æ d t ə w ɛ l k ə m h ɪ z ɡ ɑː s p əl']
print(transcription)

data_s = map_to_array('test2monostutter.flac')  
 # tokenize
input_values = processor(data_s, return_tensors="pt").input_values
 
 # retrieve logits
with torch.no_grad():
    logits = model(input_values).logits
 
 # take argmax and decode
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)
 # => should give ['m ɪ s t ɚ k w ɪ l t ɚ ɹ ɪ z ð ɪ ɐ p ɑː s əl ʌ v ð ə m ɪ d əl k l æ s ᵻ z æ n d w iː ɑːɹ ɡ l æ d t ə w ɛ l k ə m h ɪ z ɡ ɑː s p əl']
print(transcription)