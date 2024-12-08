from azureml.core import Webservice
from azureml.core import Workspace
import json
import requests

def get_prediction(img, params):
    ws = Workspace.from_config(path=r'./config.json')

    # Підключаємо сервіс
    service = Webservice(workspace=ws, name='akscloudservice')

    # Дані для тесту
    row_data = {
        "image": img.tolist(),
        'params':params

    }
    scoring_uri = service.scoring_uri

    key, _ = service.get_keys()
    headers = {"Content-Type": "application/json"}
    headers['Authorization'] = f'Bearer {key}'
    json_data = json.dumps(row_data)
    response = requests.post(scoring_uri, data=json_data, headers=headers)
    return response.json()