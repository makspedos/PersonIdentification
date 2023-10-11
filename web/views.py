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
            form.save()
            return redirect('web:home')
        else:
            form =FaceForm()

    return render(request, 'html/form.html', locals())

def home(request):
    image = Image.objects.all()
    print(image)

    context = {
        'image':image,
    }
    return render(request, 'html/home.html', context)