import cv2 as cv
from PIL import Image
import numpy as np


def detect_face(img):
    face_classifier = cv.CascadeClassifier('C:/Users/maksp/PycharmProjects/face_recognision/haarcascade_frontalface_default.xml')
    img = Image.open(img)
    opencv_image = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    grey_img = cv.cvtColor(opencv_image, cv.COLOR_BGR2GRAY)

    face = face_classifier.detectMultiScale(grey_img, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    for (x, y, w, h) in face:
        cv.rectangle(opencv_image, (x, y), (x + w, y + h), (0, 255, 0), 4)
        opencv_image = opencv_image[y:y + h, x:x + w]
    cv.imwrite(r'C:\Users\maksp\PycharmProjects\face_recognision\web\static\faces\face.png',opencv_image)

