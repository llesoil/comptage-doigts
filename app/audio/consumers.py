from channels.generic.websocket import WebsocketConsumer
from pydub import AudioSegment
from datetime import datetime

import json
import base64
import os
import numpy as np
import speech_recognition as sr

from . import models

class AudioConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()
        self.BASE_DIR = os.path.abspath(".")
        self.recognizer = sr.Recognizer()
        self.index = 0

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        response="e"
        self.index = self.index + 1
        self.position = "l"*(self.index%2==0)+"r"*(self.index%2==1)
        try:
            text_data_json = json.loads(text_data)
            audio = base64.b64decode(text_data_json['message'])
            dt = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ%f')[:-3]
            address = os.path.join(self.BASE_DIR, 'data//audio//'+dt+'.m4a')
            with open(address,'wb') as f:
                f.write(audio)
            AudioSegment.from_file(address).export(address[:-4]+'.wav', format="wav")
            os.remove(address)
            response="error"
            with sr.AudioFile(address[:-4]+'.wav') as source:
                test_file = self.recognizer.record(source)
            speech = self.recognizer.recognize_sphinx(test_file, language="fr-FR").split(" ")
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
                        response=str(count)
                    else:
                        print("Number not recognized")
                except:
                    print(word + " is not a number between 0 and 10")
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not find Sphinx Speech Recognition service; {0}".format(e))
        self.response(response)
        #save to mongoDB
        pict = models.Audio.objects.create(file_name = dt+'.wav', date = dt, pred_count = response, left_hand = (self.position =="l"), true_count = None)
        pict.save()

    def response(self, msg):

        self.send(text_data=json.dumps({
            'message': msg
        }))
