from django.shortcuts import render, redirect
from .forms import FaceForm
from .models import Image
from model_project.MyModel.MyModel import PredictionModel


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
            form.save()
            request.session['params'] = params
            return redirect('web:work_page')
        else:
            form = FaceForm()

    return render(request, 'html/all/form.html', locals())


def work_page(request):
    params = request.session.get('params','')
    image = Image.objects.all().last()
    output= model.face_detection(image.img,params)
    image = 'C:/Users/maksp/PycharmProjects/face_recognision/web/static/faces/face.png'

    print(output)
    context = {
        'image': image,
        'output': output,
    }

    return render(request, 'html/all/work_page.html', context)

