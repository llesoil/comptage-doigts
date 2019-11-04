from channels.generic.websocket import WebsocketConsumer
import json
import base64
from time import gmtime, strftime
import os
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model

class PictureConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()
        self.BASE_DIR = os.path.abspath(".")
        tf.keras.backend.clear_session()
        self.model = load_model(os.path.join(self.BASE_DIR, 'models//picture//finger_low_resolution.h5'))
        self.model._make_predict_function()
        self.img_dim = 28

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        img = base64.b64decode(text_data_json['message'])
        address =  os.path.join(self.BASE_DIR, 'data//picture//'+strftime("%Y-%m-%dT%H-%M-%S", gmtime())+'.png')
        with open(address,'wb') as f:
            f.write(img)
        img = cv2.imread(address)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        modelInput = np.array(cv2.resize(gray, (self.img_dim,self.img_dim)), dtype= np.float32)/255
        #kernel = np.ones((5,5), np.uint8)
        #img = cv2.erode(cv2.dilate(img, kernel, iterations = 1), kernel, iterations = 1)
        cv2.imshow('output', img)
        cv2.imshow('outputdim', cv2.resize(img, (self.img_dim, self.img_dim)))
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
        cv2.imwrite(address, img)
        pred = self.model.predict(modelInput.reshape(1, self.img_dim, self.img_dim, 1))
        print(np.argmax(pred))