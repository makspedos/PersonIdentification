from django.shortcuts import render, redirect
from .forms import FaceForm
from model_project.MyModel.MyModel import PredictionModel
from .models import Identification, ImageFaces
from web.clean import clean_temp
import requests
from face_recognision.custom_storage import CustomFileSystemStorage
from .saved_img_mover import moving_files
from dotenv import load_dotenv

load_dotenv()


def home(request):
    return render(request, 'html/all/home.html')


def help_page(request):
    return render(request, 'html/all/help.html')


def form_page(request):
    print(request.FILES)
    form = FaceForm(request.POST, request.FILES)
    if request.POST:
        if form.is_valid():
            clean_temp()
            data = request.POST
            age = data.get('вік', None)
            gender = data.get('стать', None)
            emotion = data.get('емоції', None)
            params = {'вік': age, 'стать': gender, 'емоції': emotion}

            request.session['params'] = params
            upload_dir = r'C:\Users\maksim\PycharmProjects\face_recognision\media\faces'

            if 'img' in request.FILES:
                img = request.FILES['img']
                fs = CustomFileSystemStorage(location=upload_dir)
                filename = fs.save('face_original.png', img)
                print(filename)
                saved_image_url = 'media/faces/face_original.png'
                request.session['img'] = {'image': saved_image_url}

            if 'image_url' in request.POST and request.POST.get('image_url') != '':
                img = request.POST.get('image_url')
                print(f'Its img:{img}')
                check_image = download_image(img, f'{upload_dir}/face_original.png')
                if not check_image:
                    form = FaceForm()
                    return redirect('web:work_page')
                saved_image_url = f'/media/faces/face_original.png'
                request.session['img'] = {'image': saved_image_url}
            return redirect('web:work_page')
        else:
            form = FaceForm()

    return render(request, 'html/all/form.html', locals())


def download_image(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print("Зображення було успішно завантажено!")
        else:
            print("Помилка при завантаженні зображення:", response.status_code)

    except Exception as e:
        print("Помилка при завантаженні зображення:")
        return False

    return True


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

    result_list, col_list = result[0], result[1]

    image = r'C:\Users\maksim\PycharmProjects\face_recognision\media\faces\face.png'
    context = {
        'image': image,
        'result_list': result_list,
        'col_list': col_list,
        'list_emotions': False,
    }
    if 'емоції' in col_list:
        list_emotions = ['Злість', 'Радість', 'Нейтральність', 'Сум', 'Здивованість']
        context['list_emotions'] = list_emotions

    if 'save_identification' in request.POST:
        file_save_path = moving_files()
        image_face = ImageFaces.objects.create(user=request.user,
                                               img=file_save_path)
        image_face.save()
        count = 1
        for i in result_list:
            age = None
            gender = 'Не задано'
            emotion = 'Не задано'
            if 'вік' in col_list:
                age = i['вік']
            if 'стать' in col_list:
                gender = i['стать']
            if 'емоції' in col_list:
                max_emotion = []
                for e in i['емоції']:
                    max_emotion.append(float(e))
                max_value = max(max_emotion)
                emotion = context['list_emotions'][max_emotion.index(max_value)]

            data_identification = Identification.objects.create(image_face=image_face, age=age, gender=gender,
                                                                emotion=emotion, face_number=count)
            data_identification.save()
            count += 1

        return redirect('web:form_page')

    return render(request, 'html/all/work_page.html', context)
