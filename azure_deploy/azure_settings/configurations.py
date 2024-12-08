from azureml.core.compute import AksCompute, ComputeTarget
import os
from azureml.core import Workspace
from azureml.core import Environment
import tensorflow as tf
from azureml.core.model import Model
from azureml.core import Webservice
from azureml.core.model import InferenceConfig

def setup_aks(ws):
    aks_name = 'my-aks-cluster'
    try:
        aks_target = ComputeTarget(workspace=ws, name=aks_name)
        print('Found existing aks cluster')
    except:
        print('Creating aks cluster')
        aks_config = AksCompute.provisioning_configuration(
            vm_size='Standard_B2ms',
            agent_count=3,
            location='eastus'
        )
        aks_target = ComputeTarget.create(workspace=ws, name=aks_name, provisioning_configuration=aks_config)
        aks_target.wait_for_completion(show_output=True)
    return aks_target


def workspace_creation():
    ws = Workspace.create(name=os.getenv('WORKSPACE_NAME'),subscription_id=os.getenv('SUBSCRIPTION_ID'),
                          resource_group=os.getenv('RESOURCE_GROUP'), create_resource_group='False', location='polandcentral')

    ws.write_config(path='.azureml')


def register_models(ws):
    age_model = Model.register(workspace=ws, model_name='age_model', model_path=r'D:\models\age.h5')
    gender_model = Model.register(workspace=ws, model_name='gender_model', model_path=r'D:\models\gender.h5')
    emotion_model = Model.register(workspace=ws, model_name='emotion_model', model_path=r'D:\models\emotion.h5')


def load_models(ws):
    if os.path.exists('./models/age.h5'):
        age_model_path = './models/age.h5'
    else:
        age_model_path = Model(ws, name='age_model').download(target_dir="./models", exist_ok=True)
    age_model = tf.keras.models.load_model(age_model_path)
    if os.path.exists('./models/gender.h5'):
        gender_model_path = './models/gender.h5'
    else:
        gender_model_path = Model(ws, name='gender_model').download(target_dir="./models", exist_ok=True)
    gender_model = tf.keras.models.load_model(gender_model_path)
    if os.path.exists('./models/emotion.h5'):
        emotion_model_path = './models/emotion.h5'
    else:
        emotion_model_path = Model(ws, name='emotion_model').download(target_dir="./models", exist_ok=True)
    emotion_model = tf.keras.models.load_model(emotion_model_path)

    return age_model, gender_model, emotion_model


def create_environment():
    env = Environment.from_conda_specification(
        name='model_environments_final',
        file_path=r'.\conda_dependencies.yml'
    )
    return env

def update_environemnt(ws):
    env_name= 'model_environments'
    current_env = Environment.get(workspace=ws, name=env_name)
    new_environment = Environment(name=env_name)
    new_environment.python.conda_dependencies_file = r'C:\Users\Maksim\PycharmProjects\face_recognision\azure_deploy\conda_dependencies.yml'
    new_environment.register(workspace=ws)
    print(f"Registered new version of environment '{env_name}'.")


def delete_or_update_service(ws, action):
    service = Webservice(workspace=ws, name='mycloudservice')
    if action == 'delete':
        service.delete()
    else:
        env = create_environment()
        inference_config = InferenceConfig(
            entry_script="./scope.py",
            environment=env
        )
        service.update(inference_config=inference_config)