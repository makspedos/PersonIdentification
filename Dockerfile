FROM python:3.11


RUN apt-get update && apt-get install -y libgl1-mesa-glx
WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./model_project/models/age/age.h5 /code/model_project/models/age/age.h5
COPY ./model_project/models/age/age.h5 /code/model_project/models/emotion/emotion.h5
COPY ./model_project/models/age/age.h5 /code/model_project/models/gender/gender-model.h5
COPY ./haarcascade_frontalface_default.xml /code/haarcascade_frontalface_default.xml

COPY . .