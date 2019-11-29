# -*- coding: utf-8 -*-
# Requires speech recognition and pocketsphinx with the french dictionary

import speech_recognition as sr
import cv2
import numpy as np

r = sr.Recognizer()

# Use the microphone instead of the previous file
#with sr.Microphone() as source:
#    print("Say something!")
#    audio = r.listen(source)

test_file = sr.AudioFile('number.wav')
#test_file = sr.AudioFile('2019-11-26T18-02-16.wav')

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
                #cv2.imshow("detection", cv2.imread("./data/picture/print/"+str(count)+".jpg"))
                #cv2.waitKey(5000)
                #cv2.destroyAllWindows()
                print("You said: " + str(count))
            else:
                print("Number not recognized")
        except:
            print(word + " is not a number between 0 and 10")
except sr.UnknownValueError:
    print("Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not find Sphinx Speech Recognition service; {0}".format(e))
