import json
import requests
import cv2

test_image = cv2.imread(r'/media/images/family.jpg')
test_image = cv2.resize(test_image, (224, 224), interpolation=cv2.INTER_AREA)

data = {
    "image": test_image.tolist(),
    'params':{'вік':'true', 'стать':'true', 'емоції': 'true'}
}


url = "http://127.0.0.1:6789/score"

response = requests.post(url, data=json.dumps(data),  headers={"Content-Type": "application/json"})

print("Response:", response.json())