

# -*- coding: utf-8 -*-
# Requires speech recognition and pocketsphinx with the french dictionary

import speech_recognition as sr
#import cv2
import numpy as np
from scipy.io import wavfile
#import matplotlib.pyplot as plt
import os

for i in range(6):
    
    address = './'+str(i)+'/'
    
    files = sorted(os.listdir(address), reverse=True)
    
    for file in files:
        if file[0:3]=="cut":
            os.remove(address+file)
        else:
            print(address+file)
            if file[len(file)-3:]!=".py":
    
                fs, data = wavfile.read(address+file)
                
                data_norm = data/np.percentile(data,99)
                n = len(data_norm)
                
                silence_threshold = 0.7
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
                print(last_word_index)
                
                first_word_index = max(0,first_word_index-5000)
                last_word_index = min(n,last_word_index+5000)
                
                real_data = data[first_word_index:last_word_index]
                
                y = (np.iinfo(np.int32).max * (real_data/np.abs(real_data).max())).astype(np.int32)
                
                #wavfile = fs, real_data
                wavfile.write(address+'cut_'+file, fs, y)
                
                #plt.scatter(np.arange(0,n,1),data)
                #plt.show()
                
    files = os.listdir(address)
    
    for file in files:
        if file[0:3]=="cut":
            
            r = sr.Recognizer()
            print(address+file)
            test_file = sr.AudioFile(address+file)
    
            with test_file as source:
                audio = r.record(source)
            
            # Speech recognition using Sphinx Speech Recognition
            try:
                speech = r.recognize_sphinx(audio, language="fr-FR").split(" ")
                number = np.array(['zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix'])
                for i in range(len(speech)):
                    try:
                        word = str(speech[i])
                        print(word)
                        if word in number:
                            count = np.where(number==word)[0][0]
                        else:
                            count = int(word)
                        if count >= 0 and count <10:
                            print("You said: " + str(count))
                        else:
                            print("Number not recognized")
                    except:
                        print(word + " is not a number between 0 and 10")
            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not find Sphinx Speech Recognition service; {0}".format(e))




































