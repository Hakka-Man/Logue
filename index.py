from itertools import count
import streamlit as st
import sounddevice as sd
import scipy as sc
import soundfile as sf
import numpy as np
from multiprocessing import Process
import requests
from streamlit_lottie import st_lottie
import pickle
import random
import phodel
import eng_to_ipa as ipa

with (open("NER/labeledParagraphs.pickle", "rb")) as openfile:
  labeledParagraphs = pickle.load(openfile)

with (open("NER/modifiableWords.pickle", "rb")) as openfile:
  modifiableWords = pickle.load(openfile)

with (open("NER/wordPosPhonemeDict.pickle", "rb")) as openfile:
  wordPosPhonemeDict = pickle.load(openfile)


def load_lottieurl(url):
  request = requests.get(url)
  if request.status_code != 200:
    return None
  return request.json()

def record():
  print("record started")
  fs = 16000  # sample rate 16000 Hz
  recording = sd.rec(int(SAMPLE_TIME * fs), samplerate=fs, channels=1)
  sd.wait()
  sc.io.wavfile.write('output.wav', fs, recording)

  # converting from wav to flac
  data, fs = sf.read('output.wav') 
  sf.write('output.flac', data, fs)
  print("record ended")

def next(prev, curr):
  st.session_state[prev] = False
  st.session_state[curr] = True
  st.experimental_rerun()

def substitute_paragraph(phoenemes):
  # paragraph = labeledParagraphs[random.randint(0,4)]
  paragraph = labeledParagraphs[0]
  paragraph_text = ""
  index = 0
  for word in paragraph:
    if word[1] == "PUNCT":
      paragraph_text = paragraph_text[0: -1]
    if word[1] in modifiableWords:
      i = index
      for j in range(len(phoenemes)):
        if (word[1], phoenemes[i]) in wordPosPhonemeDict.keys():
          possibleWords = wordPosPhonemeDict[(word[1], phoenemes[i])]
          paragraph_text += possibleWords[random.randint(0, len(possibleWords) - 1)]
          paragraph_text += " "
          index = (index + 1) % len(phoenemes)
          break
        i = (i + 1) % len(phoenemes)
      else:
        paragraph_text += (word[0] + " ")
    else:
      paragraph_text += (word[0] + " ")
  return paragraph_text
      

def predict_stutter():
  stuttered_phonemes = st.session_state.phoenemes
  stuttered_phonemes_maps = {}
  for phoneme in stuttered_phonemes:
    stuttered_phonemes_maps[phonemes] = 1
  words = SAMPLE_PARAGRAPH.split()
  processed_words = []
  for word in words:
    phonemes = ipa.convert(word)
    for phoneme in phonemes:
      if phoneme in stuttered_phonemes:
        processed_words.append("<u>" + word + "</u>")
        break
    else:
      processed_words.append(word)
  return (" ").join(processed_words)
    

SAMPLE_PARAGRAPH = """
\"Dad who is talking on the phone mentioned eating bug eggs with jam this summer. My funny and dippy cat living in the ocean likes to listen to the rhyme of the flute. This is why you don’t give him tips with carrots. Yesterday, at eight, the sky was pink. Five bees and one wolf fought with three monkeys and four birds next to the gym. A boy ended up shouting in their ears and cured the wolf’s arm with pencils and scissors. In the future, I will buy a pair of leather thongs and hide them on a beach where no one can open this treasure.\"  
"""

# time user has to read the sample paragraph
SAMPLE_TIME = 60

book_animation = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_4XmSkB.json")

# def count_down(second):
#   for i in range(second, 0, -1):
#     print(i)

# initialize state variables
if 'read_expended' not in st.session_state:
  st.session_state.read_expended = True

if 'analyze_expended' not in st.session_state:
  st.session_state.analyze_expended = False

if 'practice_expended' not in st.session_state:
  st.session_state.practice_expended = False

if 'result_expended' not in st.session_state:
  st.session_state.result_expended = False

if 'stuttered_text' not in st.session_state:
  st.session_state.stuttered_text = SAMPLE_PARAGRAPH

if 'phoenemes' not in st.session_state:
  st.session_state.phoenemes = []

if 'paragraph' not in st.session_state:
  st.session_state.paragraph = ""

st.write("""
<style>
u {
  color: red
}
</style>
""", unsafe_allow_html=True)

# hero
with st.container():
  col1, col2 = st.columns(2)
  with col1:
    st_lottie(book_animation)
  with col2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.title("AI Powered Speech Therapist")

# Task: Intro (maybe use card)
st.text("made by Alan, Henry, Willy")
st.write("This app is an AI powered digital speech therapist that helps stutterer becomes better at speaking.")

# step 1
with st.container():
  read = st.expander("Step 1.",
    expanded = st.session_state.read_expended
  )
  with read:
    st.title("Read 📖")
    st.markdown("Hello! Welcome to the first step of the therapy. In this section, please read the following paragraph so that we can detect which <u>phonemes</u> you struggle to pronounce. The paragraph is designed to test all the phonemes, so it may not make semantic sense. Please relax and click the 'Start Recording' button and start speaking when you are ready.", unsafe_allow_html=True)
    st.markdown("<strong>" + SAMPLE_PARAGRAPH + "</strong>", unsafe_allow_html=True)
    read_clicked = st.button("Start Recording",
      key = "read-button"
    )
    if read_clicked:
      # optional task: can add countdown feature on button
      # optional task: allow user to download the recorded audio
      # record()
      t, t_s = phodel.getTranscription(SAMPLE_PARAGRAPH)
      phoenemes = phodel.getPhonemes(t, t_s)
      print(phoenemes)
      st.session_state.phoenemes = phoenemes
      paragraph = substitute_paragraph(phoenemes)
      st.session_state.paragraph = paragraph
      print(paragraph)

      # task: predict_stutter()
      next("read_expended", "analyze_expended")

# step 2
with st.container():
  read = st.expander("Step 2.",
    expanded = st.session_state.analyze_expended
  )
  with read:
    st.title("Analyze 📋")
    st.write("Words you stuttered on:")
    st.markdown(predict_stutter(), unsafe_allow_html=True) # Task: underline words stuttered on
    st.write("Phonemes you stuttered on:")
    st.text(st.session_state.phoenemes) # Task: show phonemes
    analyze_clicked = st.button("Next",
      key = "analyze-button"
    )
    if analyze_clicked:
      next("analyze_expended", "practice_expended")

# step 3
with st.container():
  read = st.expander("Step 3.",
    expanded = st.session_state.practice_expended
  )
  with read:
    st.title("Practice 🎙")
    st.write("Our AI generated a paragraph below based on the phonemes you stuttered on the most. The paragraph is designed to be a little diffcult for you to read because we reused phonemes you stuttered on the most when generating the paragraph. Practice reading out the paragraph will help you from stuttering. Click the 'Start Recording' button and start the practice when you are ready. You can do it!")
    st.markdown("<strong>" + st.session_state.paragraph + "</strong>", unsafe_allow_html=True)
    practice_clicked = st.button("Next",
      key = "practice-button"
    )
    if practice_clicked:
      next("practice_expended", "result_expended")
  
# result
with st.container():
  read = st.expander("Result",
    expanded = st.session_state.result_expended
  )
  with read:
    st.title("Result 🤗")

# Footer
# with st.container():
#   st.caption("Animation made by [Alessio Ciancio](https://lottiefiles.com/alessiociancio) from www.lottiefiles.com")