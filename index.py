from itertools import count
import streamlit as st
import sounddevice as sd
import scipy as sc
import soundfile as sf
import numpy as np
from multiprocessing import Process
import requests
from streamlit_lottie import st_lottie

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

SAMPLE_PARAGRAPH = """
\"Simply put, a paragraph is a collection of sentences all related to a central topic, idea, or theme. Paragraphs act as structural tools for writers to organize their thoughts into an ideal progression, and they also help readers process those thoughts effortlessly. Imagine how much harder reading and writing would be if everything was just one long block of text.\"  
\- __Grammarly - What is a paragraph?__ 
"""

# time user has to read the sample paragraph
SAMPLE_TIME = 2

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

# intro
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
    st.title("Lionel Logue")
    st.text("2022 AI powered speech therapist")
    # st.caption("AI powered speech therapist")

# step 1
with st.container():
  read = st.expander("Step 1.",
    expanded = st.session_state.read_expended
  )
  with read:
    st.title("Read 📖")
    st.write(SAMPLE_PARAGRAPH)
    read_clicked = st.button("Start Recording",
      key = "read-button"
    )
    if read_clicked:
      # optional task: can add countdown feature on button
      # optional task: allow user to download the recorded audio
      record()
      next("read_expended", "analyze_expended")

# step 2
with st.container():
  read = st.expander("Step 2.",
    expanded = st.session_state.analyze_expended
  )
  with read:
    st.title("Analyze 📋")
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
with st.container():
  st.caption("Animation made by [Alessio Ciancio](https://lottiefiles.com/alessiociancio) from www.lottiefiles.com")