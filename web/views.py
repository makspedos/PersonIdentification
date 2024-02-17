import cv2
from django.shortcuts import render, redirect
from .forms import FaceForm
from .models import Image
from model_project.MyModel.MyModel import PredictionModel
from django.core.files.storage import FileSystemStorage
from .models import Question, Answer

def home(request):
    return render(request, 'html/all/home.html')


def help_page(request):
    questions = Question.objects.all()
    anwers = Answer.objects.all()
    return render(request, 'html/all/help.html', locals())

def form_page(request):
    form = FaceForm(request.POST, request.FILES)
    if request.POST:
        if form.is_valid():
            data = request.POST
            age = data.get('age', None)
            gender = data.get('gender', None)
            emotion = data.get('emotion', None)
            params = {'вік': age, 'стать': gender, 'емоції': emotion}

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
    params = request.session.get('params', '')
    img = request.session.get('img', '')
    model = PredictionModel()
    result_list, col_list = model.face_detection(params, img)

    image = 'C:/Users/maksp/PycharmProjects/face_recognision/web/static/faces/face.png'
    context = {
        'image': image,
        'result_list': result_list,
        'col_list': col_list,
        'list_emotions': False,
    }
    if 'емоції' in col_list:
        list_emotions = ['Злість', 'Радість', 'Нейтральність', 'Сум', 'Здивованість']
        context['list_emotions'] = list_emotions

    return render(request, 'html/all/work_page.html', context)


