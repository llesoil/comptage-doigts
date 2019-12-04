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

class PictureConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()
        self.BASE_DIR = os.path.abspath(".")
        tf.keras.backend.clear_session()
        self.model = load_model(os.path.join(self.BASE_DIR, 'models//picture//finger_low_resolution_v3.h5'))
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
            address =  os.path.join(self.BASE_DIR, 'data//picture//'+ dt +'.png')
            with open(address,'wb') as f:
                f.write(img)
            img = cv2.imread(address)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            modelInput = np.array(cv2.resize(gray, (self.img_dim,self.img_dim)), dtype= np.float32)/255
            # optionnally, add a dilate and erode step to remove some background substraction errors
            # just uncomment the two following lines
            #kernel = np.ones((5,5), np.uint8)
            #img = cv2.erode(cv2.dilate(img, kernel, iterations = 1), kernel, iterations = 1)
            cv2.imwrite(address, img)
            pred = self.model.predict(modelInput.reshape(1, self.img_dim, self.img_dim, 1))
            self.index = self.index + 1
            self.position = "l"*(self.index%2==0)+"r"*(self.index%2==1)
            pred_count = np.argmax(pred)            
            response = self.position+str(pred_count)
        except:
            print("Unable to predict")
        self.response(response)
        #save to mongoDB
        pict = models.Picture.objects.create(file_name = dt+'.png', date = dt, pred_count = pred_count, left_hand = (self.position =="l"), true_count = None)
        pict.save()

    def response(self, msg):

        self.send(text_data=json.dumps({
            'message': msg
        }))
