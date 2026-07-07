import json
import logging
import os
from pathlib import Path

import requests
from PIL import Image, ImageDraw

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import numpy as np
    import tensorflow as tf
    from keras.applications.resnet50 import preprocess_input
    from keras.models import load_model
except ImportError:
    np = None
    tf = None
    preprocess_input = None
    load_model = None

try:
    from azure_deploy import predict_cloud
    from azureml.core import Webservice, Workspace
except ImportError:
    predict_cloud = None
    Webservice = None
    Workspace = None


logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = Path(os.getenv("MODEL_DIR", BASE_DIR / "models"))


class PredictionModel:
    """Prediction wrapper for Azure ML, local Keras models, or explicit demo fallback."""

    _instance = None
    AGE_PARAM = "age"
    GENDER_PARAM = "gender"
    EMOTION_PARAM = "emotion"

    def __new__(cls, *args, **kwargs):
        """Keep one loaded model wrapper per Django process."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize cloud, local, or demo inference backends."""
        if self._initialized:
            return

        self.cloud_connection = self.check_cloud_connection()
        self.age_model = None
        self.gender_model = None
        self.emotion_model = None
        self.cascade = None

        if self.cloud_connection:
            logger.info("Prediction model initialized with Azure ML inference.")
        elif self._keras_available():
            self.age_model = self._load_local_model("AGE_MODEL_PATH", MODEL_DIR / "age.h5")
            self.gender_model = self._load_local_model("GENDER_MODEL_PATH", MODEL_DIR / "gender.h5")
            self.emotion_model = self._load_local_model("EMOTION_MODEL_PATH", MODEL_DIR / "emotion.h5")
        else:
            logger.warning("ML dependencies are not installed; using demo inference fallback.")

        if cv2 is not None:
            cascade_path = Path(os.getenv("HAAR_CASCADE_PATH", BASE_DIR / "ml" / "haarcascade_frontalface_default.xml"))
            cascade = cv2.CascadeClassifier(str(cascade_path))
            if not cascade.empty():
                self.cascade = cascade
            else:
                logger.warning("Haar cascade file not found or invalid: %s", cascade_path)

        self._initialized = True

    def _keras_available(self):
        """Return whether optional TensorFlow/Keras dependencies are installed."""
        return np is not None and tf is not None and preprocess_input is not None and load_model is not None

    def _load_local_model(self, env_name, default_path):
        """Load a local Keras model from an environment override or default path."""
        model_path = Path(os.getenv(env_name, default_path))
        if not model_path.exists():
            logger.warning("Local model file is missing: %s", model_path)
            return None
        return load_model(model_path)

    def check_cloud_connection(self):
        """Check whether the optional Azure ML endpoint is configured and reachable."""
        if predict_cloud is None or Workspace is None or Webservice is None:
            return False

        try:
            url = os.getenv("AZURE_URL")
            if not url:
                return False

            config_path = os.getenv("AZUREML_CONFIG_PATH", str(BASE_DIR / "azure_deploy" / "config.json"))
            service_name = os.getenv("AZUREML_SERVICE_NAME", "akscloudservice")
            ws = Workspace.from_config(path=config_path)
            service = Webservice(workspace=ws, name=service_name)
            key, _ = service.get_keys()
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
        except Exception as exc:
            logger.info("Azure ML inference is unavailable: %s", exc)
            return False

    def face_detection(self, params, img):
        """Detect faces and return requested predictions for the uploaded image."""
        image_path = Path(img.get("image_path", ""))
        if not image_path.exists():
            logger.warning("Input image does not exist: %s", image_path)
            return False

        if cv2 is not None and self.cascade is not None:
            return self._opencv_face_detection(image_path, params)

        return self._demo_face_detection(image_path, params)

    def _opencv_face_detection(self, image_path, params):
        """Use OpenCV Haar cascades to annotate detected faces."""
        try:
            test_image = cv2.imread(str(image_path))
            if test_image is None:
                return self._demo_face_detection(image_path, params)

            gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
            faces = self.cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 0:
                logger.warning("No faces detected; using full image as demo region.")
                return self._demo_face_detection(image_path, params)

            result_params = []
            for face_count, (x, y, w, h) in enumerate(faces, start=1):
                cv2.rectangle(test_image, (x, y), (x + w, y + h), (203, 12, 255), 2)
                img_gray = gray[y:y + h, x:x + w]
                result_params.append(self.model_prediction(img_gray, params))
                cv2.putText(test_image, str(face_count), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            output_path = BASE_DIR / "media" / "faces" / "face.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(output_path), test_image)

            col_list = list(result_params[0].keys()) if result_params else []
            return result_params, col_list
        except Exception as exc:
            logger.warning("OpenCV face detection failed; using demo fallback: %s", exc)
            return self._demo_face_detection(image_path, params)

    def _demo_face_detection(self, image_path, params):
        """Create a deterministic fallback result when ML dependencies are absent."""
        output_path = BASE_DIR / "media" / "faces" / "face.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(image_path) as image:
            image = image.convert("RGB")
            draw = ImageDraw.Draw(image)
            width, height = image.size
            margin_x = max(width // 10, 4)
            margin_y = max(height // 10, 4)
            draw.rectangle(
                [margin_x, margin_y, width - margin_x, height - margin_y],
                outline=(203, 12, 255),
                width=max(min(width, height) // 100, 2),
            )
            image.save(output_path)

        result = self.demo_prediction(params)
        if not result:
            return False
        return [result], list(result.keys())

    def model_prediction(self, img_gray, params):
        """Run cloud or local model inference for a single face crop."""
        if self.cloud_connection:
            result = json.loads(predict_cloud.get_prediction(img_gray, params))
            output_age = result["age"]
            output_gender = result["gender"]
            output_emotion = result["emotion"]
        elif self._keras_available():
            image = cv2.resize(img_gray, (224, 224), interpolation=cv2.INTER_AREA)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            image_shaped = np.reshape(image, (1, 224, 224, 3)) / 255.0

            output_age = 0
            output_gender = 0
            output_emotion = 0

            if params.get(self.AGE_PARAM) == "true" and self.age_model is not None:
                output_age = self.age_model.predict(image_shaped)

            if params.get(self.GENDER_PARAM) == "true" and self.gender_model is not None:
                output_gender = self.gender_model.predict(image_shaped)

            if params.get(self.EMOTION_PARAM) == "true" and self.emotion_model is not None:
                emotion_image = preprocess_input(image)
                emotion_image = tf.expand_dims(emotion_image, 0)
                output_emotion = self.emotion_model.predict(emotion_image)[0]
        else:
            return self.demo_prediction(params)

        result_params = {
            self.AGE_PARAM: int(output_age[0][0]) if output_age != 0 else 0,
            self.GENDER_PARAM: self.gender_convert(output_gender),
            self.EMOTION_PARAM: self.emotion_convert(output_emotion),
        }

        if any(value == 0 for value in result_params.values()):
            fallback = self.demo_prediction(params)
            for key, value in fallback.items():
                result_params[key] = result_params.get(key) or value

        return {key: value for key, value in result_params.items() if value != 0}

    def demo_prediction(self, params):
        """Return explicit placeholders for requested predictions without weights."""
        result = {}
        if params.get(self.AGE_PARAM) == "true":
            result[self.AGE_PARAM] = "Model not configured"
        if params.get(self.GENDER_PARAM) == "true":
            result[self.GENDER_PARAM] = "Model not configured"
        if params.get(self.EMOTION_PARAM) == "true":
            result[self.EMOTION_PARAM] = ["n/a", "n/a", "n/a", "n/a", "n/a"]
        return result

    def gender_convert(self, output_gender):
        """Convert the binary model output into a display label."""
        if output_gender == 0:
            return 0
        return "male" if output_gender[0][0] < 0.5 else "female"

    def emotion_convert(self, output_emotion):
        """Format emotion probabilities as percentage strings."""
        if isinstance(output_emotion, int):
            return 0
        return [f"{value * 100:.2f}" for value in output_emotion]