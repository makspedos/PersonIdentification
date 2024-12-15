from azureml.core import Workspace
from azureml.core.webservice import LocalWebservice, AciWebservice
from dotenv import load_dotenv
from azure_settings.configurations import *

load_dotenv()


def local_deploy(ws):
    age_model = Model(ws, name='age_model')
    gender_model = Model(ws, name='gender_model')
    emotion_model = Model(ws, name='emotion_model')

    env = create_environment()
    inference_config = InferenceConfig(
        entry_script="./scope.py",
        environment=env
    )
    deployment_config = LocalWebservice.deploy_configuration(6789)

    service = Model.deploy(
        workspace=ws,
        name='localservice',
        models=[age_model, gender_model, emotion_model],
        inference_config=inference_config,
        deployment_config=deployment_config,
        overwrite=True,
    )

    service.wait_for_deployment(show_output=True)
    print(service.get_logs())


def cloud_deploy(ws):
    age_model = Model(ws, name='age_model')
    gender_model = Model(ws, name='gender_model')
    emotion_model = Model(ws, name='emotion_model')

    env = create_environment()
    inference_config = InferenceConfig(
        entry_script="./scope.py",
        environment=env
    )

    deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=4, auth_enabled=True)
    service = Model.deploy(
        workspace=ws,
        name='mycloudservice',
        models=[age_model, gender_model, emotion_model],
        inference_config=inference_config,
        deployment_config=deployment_config,
        overwrite=True,
    )
    print(service.get_logs())
    service.wait_for_deployment(show_output=True, timeout_sec=600)

#ws = Workspace.from_config(path=r'C:\Users\Maksim\PycharmProjects\face_recognision\azure_deploy\config.json')
#cloud_deploy_kubernetes()
#local_deploy()
#create_environment()
#cloud_deploy()
#delete_or_update_service('delete')
#register_models(ws)
