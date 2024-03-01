from django.shortcuts import render, redirect
from .forms import FaceForm
from model_project.MyModel.MyModel import PredictionModel
from django.core.files.storage import FileSystemStorage
from .models import Question, Answer
from .clean import clean_temp
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
    result = model.face_detection(params, img)
    if result is False:
        context = {
            'image': False,
        }
        return render(request, 'html/all/work_page.html', context)

    result_list, col_list = result[0],result[1]

    image = r'C:\Users\maksp\PycharmProjects\face_recognision\media\faces\face.png'
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

def clean_page(request):
    clean_temp()
    return redirect('web:form_page')


