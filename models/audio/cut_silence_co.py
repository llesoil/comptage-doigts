

# -*- coding: utf-8 -*-
# Requires speech recognition and pocketsphinx with the french dictionary

#import speech_recognition as sr
import cv2
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

import os

files = os.listdir('.')

fs, data = wavfile.read('with_silence.wav')

data_norm = data/np.percentile(data,99)
n = len(data_norm)

silence_threshold = 0.8
step = 50

first_word = False
first_word_index = 0
last_word = False
last_word_index = 60000

for i in np.arange(step,n-step,step):
    
    if not first_word:
        if np.mean(np.abs(data_norm[i-step:i+step])) > silence_threshold:
            first_word = True
            first_word_index = i
    if not last_word:
        if np.mean(np.abs(data_norm[n-i-step:n-i+step])) > silence_threshold:
            last_word = True
            last_word_index = n-i

print(first_word_index)
#print(last_word_index)

first_word 

real_data = data[first_word_index-5000:last_word_index+5000]

#wavfile = fs, real_data
wavfile.write('silence_cut.wav', fs, real_data)

#plt.scatter(np.arange(0,n,1),data)
#plt.show()







