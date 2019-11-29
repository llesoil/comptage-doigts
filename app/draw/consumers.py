from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from tensorflow.keras.models import load_model

import json
import base64
import os
import cv2
import numpy as np
import tensorflow as tf

from . import models

class DrawConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()
        self.BASE_DIR = os.path.abspath(".")
        tf.keras.backend.clear_session()
        self.model = load_model(os.path.join(self.BASE_DIR, 'models//draw//mnist_05.h5'))
        print(self.model)
        self.model._make_predict_function()
        self.img_dim = 28
        self.index = 0

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        response="error"
        try:
            text_data_json = json.loads(text_data)
            img = base64.b64decode(text_data_json['message'])
            dt = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ%f')[:-3]
            address =  os.path.join(self.BASE_DIR, 'data//draw//'+ dt +'.png')
            with open(address,'wb') as f:
                f.write(img)
            gray = cv2.imread(address,0)
            modelInput = np.array(cv2.resize(gray, (self.img_dim,self.img_dim)), dtype= np.float32)
            test = np.zeros(modelInput.shape[0]*modelInput.shape[1]).reshape(modelInput.shape[0], modelInput.shape[1])
            for i in range(modelInput.shape[0]):
                for j in range(modelInput.shape[1]):
                    if modelInput[i][j]>0:
                        test[i][j] = 1
            pred = self.model.predict(test.reshape(1, self.img_dim, self.img_dim, 1))
            pred_count = np.argmax(pred)
            response = str(pred_count)
            #save to mongoDB
            pict = models.Draw.objects.create(file_name = dt+'.png', date = dt, pred_count = response, true_count = None)
            pict.save()
        except:
            print("Unable to predict")
        self.response(response)


    def response(self, msg):

        self.send(text_data=json.dumps({
            'message': msg
        }))
