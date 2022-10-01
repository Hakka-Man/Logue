from itertools import count
import streamlit as st
import sounddevice as sd
import scipy as sc
import soundfile as sf
import numpy as np
from multiprocessing import Process

SAMPLE_PARAGRAPH = """
\"Simply put, a paragraph is a collection of sentences all related to a central topic, idea, or theme. Paragraphs act as structural tools for writers to organize their thoughts into an ideal progression, and they also help readers process those thoughts effortlessly. Imagine how much harder reading and writing would be if everything was just one long block of text.\"  
\- __Grammarly - What is a paragraph?__ 
"""

# time user has to read the sample paragraph
SAMPLE_TIME = 2


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

  # set session expended values
  st.session_state.read_expended = False
  st.session_state.show_stutter_expended = True
  st.experimental_rerun()

def next():
  st.session_state.show_stutter_expended = False
  st.experimental_rerun()

# def count_down(second):
#   for i in range(second, 0, -1):
#     print(i)

if 'read_expended' not in st.session_state:
  st.session_state.read_expended = True

if 'show_stutter_expended' not in st.session_state:
  st.session_state.show_stutter_expended = False

with st.container():
  read = st.expander("Step 1.",
    expanded = st.session_state.read_expended
  )
  with read:
    st.title("Read 📖")
    st.write(SAMPLE_PARAGRAPH)
    record_clicked = st.button("Start Recording")
    if record_clicked:
      # optinal task: can add countdown feature on button
      record()

with st.container():
  read = st.expander("Step 2.",
    expanded = st.session_state.show_stutter_expended
  )
  with read:
    st.title("Read 📖")
    next_clicked = st.button("Next")
    if next_clicked:
      # add countdown
      next()