from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import torch
import eng_to_ipa as ipa
import soundfile as sf

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-lv-60-espeak-cv-ft")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-lv-60-espeak-cv-ft")

def map_to_array(batch):
    speech_array, _ = sf.read(batch)
    return speech_array

def getTranscription(originalText):
    data = map_to_array('output.flac')  
    input_values = processor(data, return_tensors="pt").input_values
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription_s = processor.batch_decode(predicted_ids)
    transcription  = [ipa.convert(originalText)]
    return transcription, transcription_s

def getPhonemes(trans, trans_s):
    searched = set()
    searched.add(" ")
    fluencyScore = 0
    stutterPhonemes = []
    for phoneme in trans[0]:
        if phoneme not in searched:
            searched.add(phoneme)
            og = trans[0].count(phoneme)
            vc = trans_s[0].count(phoneme)
            score = float(vc) / float(og)
            if score > 1.5:
                stutterPhonemes.append(phoneme)
                fluencyScore += 1
                if score > 2:
                    fluencyScore += 1
    fluencyScore = (len(searched)  - fluencyScore) / len(searched)
    return stutterPhonemes, fluencyScore
