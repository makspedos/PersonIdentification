import cv2
from django.shortcuts import render, redirect
from .forms import FaceForm
from .models import Image
from model_project.MyModel.MyModel import PredictionModel
from django.core.files.storage import FileSystemStorage

model = PredictionModel()

def form_page(request):
    form = FaceForm(request.POST, request.FILES)
    if request.POST:
        if form.is_valid():
            data =request.POST
            age = data.get('age',None)
            gender = data.get('gender',None)
            emotion = data.get('emotion', None)
            params = {'age':age, 'gender':gender, 'emotion': emotion}

            request.session['params'] = params
            img = request.FILES['img']


            upload_dir = r'C:\Users\maksp\PycharmProjects\face_recognision\media\faces'
            fs = FileSystemStorage(location=upload_dir)
            filename = fs.save(img.name, img)

            saved_image_url = fs.url(filename)
            request.session['img'] = {'image': saved_image_url}

            return redirect('web:work_page')
        else:
            form = FaceForm()

    return render(request, 'html/all/form.html', locals())


def work_page(request):
    params = request.session.get('params','')
    img = request.session.get('img', '')
    output= model.face_detection(params, img)
    image = 'C:/Users/maksp/PycharmProjects/face_recognision/web/static/faces/face.png'

    context = {
        'image': image,
        'output': output,
    }

    return render(request, 'html/all/work_page.html', context)

