import numpy as np
import cv2
from keras.models import *
from keras.applications.resnet50 import preprocess_input
import tensorflow as tf


class PredictionModel():
    def __init__(self):
        self.age_model = load_model(r'C:\Users\maksp\PycharmProjects\face_recognision\model_project\models\age\age.h5')
        self.gender_model = load_model(
            r'C:\Users\maksp\PycharmProjects\face_recognision\model_project\models\gender\gender-model.h5')
        self.emotion_model = load_model(
            r'C:\Users\maksp\PycharmProjects\face_recognision\model_project\models\emotion\emotion.h5')
        self.cascade = cv2.CascadeClassifier(
            'C:/Users/maksp/PycharmProjects/face_recognision/haarcascade_frontalface_default.xml')

    def face_detection(self, params, img):
        test_image = cv2.imread(f'C:/Users/maksp/PycharmProjects/face_recognision{img["image"]}')
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, 1.3, 5)
        face_count = 0
        result_params=[]

        for (x, y, w, h) in faces:
            face_count = face_count + 1
            cv2.rectangle(test_image, (x, y), (x + w, y + h), (203, 12, 255), 2)
            img_gray = gray[y:y + h, x:x + w]
            result_params.append(self.model_prediction(img_gray, params))
            col = (0, 255, 0)
            cv2.putText(test_image, str(face_count), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, col, 2)
        cv2.imwrite(r'C:\Users\maksp\PycharmProjects\face_recognision\web\static\faces\face.png', test_image)
        col_list = list(result_params[0].keys())
        return result_params, col_list

    def model_prediction(self, img_gray, params):
        output_age = 0
        output_emotion = 0
        output_gender = 0
        result_params = {}
        image = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        image_shaped = np.reshape(image, (1, 224, 224, 3))
        image_shaped = image_shaped / 255.0
        if params['вік'] == 'true':
            output_age = self.age_model.predict(image_shaped)[0][0]
            output_age = int(output_age)

        if params['стать'] == 'true':
            output_gender = self.gender_model.predict(image_shaped)[0][0]
            output_gender = self.gender_convert(output_gender)

        if params['емоції'] == 'true':
            emotion_image = tf.expand_dims(image, 0)
            emotion_image = preprocess_input(emotion_image)
            output_emotion = self.emotion_model.predict(emotion_image)[0]
            output_emotion = self.emotion_convert(output_emotion)




        result_params['вік'] = output_age
        result_params['стать'] = output_gender
        result_params['емоції'] = output_emotion

        result_params = {key: value for key, value in result_params.items() if value != 0}
        return result_params

    def gender_convert(self, output_gender):
        return 'Чоловік' if output_gender < 0.5 else 'Жінка'

    # def emotion_convert(self, output_emotion):
    #     key_emotion = ['Злість', 'Радість', 'Нейтральність', 'Сум', 'Здивованість']
    #     values_emotion = []
    #     for i in output_emotion:
    #         i = f"{i:.10f}"
    #
    #         values_emotion.append(i)
    #     output_emotion = dict(zip(key_emotion, values_emotion))
    #     return output_emotion

    def emotion_convert(self, output_emotion):
        values_emotion = []
        for i in output_emotion:
            i = f"{i:.10f}"

            values_emotion.append(i)
        return values_emotion