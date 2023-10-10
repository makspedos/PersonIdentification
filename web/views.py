from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import FaceForm
from .models import Image
# Create your views here.
def test(request):
    return render(request, 'html/test.html')

def form_page(request):
    form = FaceForm(request.POST, request.FILES)
    if request.POST:
        print('first point')
        if form.is_valid():
            data= request.POST
            img = data.get('img', '')
            print(img)
            Image.objects.create(img=img)
            return redirect('/home/')
        else:
            form =FaceForm()

    return render(request, 'html/form.html', locals())

def home(request):
    img = Image.objects.last()
    return render(request, 'html/home.html', locals())