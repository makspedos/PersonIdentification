import json
import os
import numpy as np
import cv2
import requests
from keras.models import *
from keras.applications.resnet50 import preprocess_input
import tensorflow as tf
from azure_deploy import predict_cloud
from dotenv import load_dotenv
from azureml.core import Webservice
from azureml.core import Workspace

load_dotenv()

class PredictionModel():
    """
    PredictionModel uses cloud models to predict but if connection fails it will load local models instead
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        self.cloud_connection = False
        result_connection = self.check_cloud_connection()
        if not result_connection:
            if self._initialized:
                return

            self.age_model = load_model(r'D:\models\age.h5')
            self.gender_model = load_model(
                r'D:\models\gender.h5')
            self.emotion_model = load_model(
                r'D:\models\emotion.h5')

            self._initialized = True
        else:
            print('I initialized cloud')
            self.cloud_connection = True
        self.cascade = cv2.CascadeClassifier(
            'C:/Users/maksim/PycharmProjects/face_recognision/haarcascade_frontalface_default.xml')

    def check_cloud_connection(self):
        try:
            url = os.getenv('AZURE_URL')
            if not url:
                print("AZURE_URL is not set")
                return False

            ws = Workspace.from_config(path=r'./config.json')
            service = Webservice(workspace=ws, name='mycloudservice')
            key, _ = service.get_keys()
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
            response = requests.get(url, headers=headers)
            print(f"Response code: {response.status_code}")

        except Exception as e:
            print(f"Error: {e}")
            return False
        print(f'Respond status: {response.status_code}')
        return response.status_code == 200

    def face_detection(self, params, img):
        try:
            test_image = cv2.imread(f'C:/Users/maksim/PycharmProjects/face_recognision/{img["image"]}')
            gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)

            faces = self.cascade.detectMultiScale(gray, 1.3, 5)
            if faces is None:
                return False
            face_count = 0
            result_params=[]

            for (x, y, w, h) in faces:
                face_count = face_count + 1
                cv2.rectangle(test_image, (x, y), (x + w, y + h), (203, 12, 255), 2)
                img_gray = gray[y:y + h, x:x + w]
                result_params.append(self.model_prediction(img_gray, params))
                col = (0, 255, 0)
                cv2.putText(test_image, str(face_count), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, col, 2)
            cv2.imwrite(r'C:\Users\maksim\PycharmProjects\face_recognision\media\faces\face.png', test_image)

            if not result_params:
                print("Error: No results from model prediction.")
                return False

            col_list = list(result_params[0].keys())

        except Exception as e:
            print(f"Error: {e}")
            return False

        return result_params, col_list

    def model_prediction(self, img_gray, params):
        output_age = 0
        output_emotion = 0
        output_gender = 0
        result_params = {}

        image = cv2.resize(img_gray, (224, 224), interpolation=cv2.INTER_AREA)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        # Get result from cloud models
        if self.cloud_connection:
            result = predict_cloud.get_prediction(image, params)
            result = json.loads(result)
            output_age = result['age']
            output_gender = result['gender']
            output_emotion =result['emotion']

        else:
            image_shaped = np.reshape(image, (1, 224, 224, 3))
            image_shaped = image_shaped / 255.0

            if params['вік'] == 'true':
                output_age = self.age_model.predict(image_shaped)

            if params['стать'] == 'true':
                output_gender = self.gender_model.predict(image_shaped)

            if params['емоції'] == 'true':
                emotion_image = preprocess_input(image)
                emotion_image = tf.expand_dims(emotion_image, 0)
                output_emotion = self.emotion_model.predict(emotion_image)[0]

        result_params['вік'] = int(output_age[0][0]) if output_age !=0 else 0
        result_params['стать'] = self.gender_convert(output_gender)
        result_params['емоції'] = self.emotion_convert(output_emotion)
        result_params = {key: value for key, value in result_params.items() if value != 0}
        return result_params

    def gender_convert(self, output_gender):
        if output_gender == 0:
            return 0
        else:
            return 'Чоловік' if output_gender[0][0] < 0.5 else 'Жінка'

    def emotion_convert(self, output_emotion):
        print(output_emotion)
        if type(output_emotion) == int:
            return 0
        else:
            values_emotion = []
            for i in output_emotion:
                i = f"{i * 100:.2f}"
                values_emotion.append(i)
            return values_emotion