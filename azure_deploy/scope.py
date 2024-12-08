import json
import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.applications.resnet50 import preprocess_input


def init():
    global age_model, gender_model, emotion_model

    model_dir = os.getenv('AZUREML_MODEL_DIR')

    # Завантаження моделі для визначення віку
    age_path = os.path.join(model_dir, 'age_model/1/age.h5')
    if not os.path.exists(age_path):
        raise FileNotFoundError(f"Age model not found at {age_path}")
    age_model = tf.keras.models.load_model(age_path)

    # Завантаження моделі для визначення статі
    gender_path = os.path.join(model_dir, 'gender_model/1/gender.h5')
    if not os.path.exists(gender_path):
        raise FileNotFoundError(f"Gender model not found at {gender_path}")
    gender_model = tf.keras.models.load_model(gender_path)

    # Завантаження моделі для визначення емоцій
    emotion_path = os.path.join(model_dir, 'emotion_model/1/emotion.h5')
    if not os.path.exists(emotion_path):
        raise FileNotFoundError(f"Emotion model not found at {emotion_path}")
    emotion_model = tf.keras.models.load_model(emotion_path)

def run(data):
    predictions = {}
    try:
        input_data = json.loads(data)
        original_image = np.array(input_data['image'])
        params = input_data['params']

        img_data = np.reshape(original_image, (1, 224, 224, 3))
        img_data = img_data / 255.0

        if params['вік'] == 'true':
            predictions['age'] = age_model.predict(img_data).tolist()
        else:
            predictions['age'] = 0
        if params['стать']=='true':
            predictions['gender'] = gender_model.predict(img_data).tolist()
        else:
            predictions['gender'] = 0
        if params['емоції'] == 'true':
            emotion_image = preprocess_input(original_image)
            emotion_image = tf.expand_dims(emotion_image, 0)
            predictions['emotion'] = emotion_model.predict(emotion_image)[0].tolist()
        else:
            predictions['emotion'] = 0
        return json.dumps(predictions)
    except Exception as e:
        return json.dumps({"error": str(e)})
