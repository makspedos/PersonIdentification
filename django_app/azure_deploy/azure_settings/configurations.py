import os
from pathlib import Path

import tensorflow as tf
from azureml.core import Environment, Webservice, Workspace
from azureml.core.model import InferenceConfig, Model


BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = Path(os.getenv("MODEL_DIR", BASE_DIR / "models"))


def workspace_creation():
    ws = Workspace.create(
        name=os.getenv("WORKSPACE_NAME"),
        subscription_id=os.getenv("SUBSCRIPTION_ID"),
        resource_group=os.getenv("RESOURCE_GROUP"),
        create_resource_group=False,
        location=os.getenv("AZURE_LOCATION", "polandcentral"),
    )
    ws.write_config(path=BASE_DIR / ".azureml")
    return ws


def register_models(ws):
    Model.register(workspace=ws, model_name="age_model", model_path=str(MODEL_DIR / "age.h5"))
    Model.register(workspace=ws, model_name="gender_model", model_path=str(MODEL_DIR / "gender.h5"))
    Model.register(workspace=ws, model_name="emotion_model", model_path=str(MODEL_DIR / "emotion.h5"))


def load_models(ws):
    model_dir = BASE_DIR / "models"
    age_model_path = model_dir / "age.h5"
    gender_model_path = model_dir / "gender.h5"
    emotion_model_path = model_dir / "emotion.h5"

    if not age_model_path.exists():
        age_model_path = Path(Model(ws, name="age_model").download(target_dir=str(model_dir), exist_ok=True))
    if not gender_model_path.exists():
        gender_model_path = Path(Model(ws, name="gender_model").download(target_dir=str(model_dir), exist_ok=True))
    if not emotion_model_path.exists():
        emotion_model_path = Path(Model(ws, name="emotion_model").download(target_dir=str(model_dir), exist_ok=True))

    return (
        tf.keras.models.load_model(age_model_path),
        tf.keras.models.load_model(gender_model_path),
        tf.keras.models.load_model(emotion_model_path),
    )


def create_environment():
    return Environment.from_conda_specification(
        name="model_environment",
        file_path=str(BASE_DIR / "azure_deploy" / "conda_dependencies.yml"),
    )


def update_environment(ws):
    env_name = "model_environment"
    new_environment = Environment(name=env_name)
    new_environment.python.conda_dependencies_file = str(BASE_DIR / "azure_deploy" / "conda_dependencies.yml")
    new_environment.register(workspace=ws)
    print(f"Registered new version of environment '{env_name}'.")


def delete_or_update_service(ws, action):
    service = Webservice(workspace=ws, name=os.getenv("AZUREML_SERVICE_NAME", "mycloudservice"))
    if action == "delete":
        service.delete()
    else:
        service.update(
            inference_config=InferenceConfig(
                entry_script="./scope.py",
                environment=create_environment(),
            )
        )