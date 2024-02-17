from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import get_user_model

class SignUpPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "account/signup.html"


class AccountProfileView(generic.ListView):
    template_name = "account/profile.html"
    model = get_user_model()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class AccountChangePassword(generic.FormView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('accounts:profile')
    template_name =  'account/password_change.html'

    def post(self, request):
        form = CustomPasswordChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')  # Redirect to the user's profile or any other appropriate page
        return render(request, self.template_name, {'form': form})


class AccountChangeUsername(generic.FormView):
    form_class = CustomUserChangeForm
    template_name = "account/username_change.html"
    success_url = reverse_lazy('accounts:profile')


    def post(self, request):
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')  # Redirect to the user's profile or any other appropriate page
        return render(request, self.template_name, {'form': form})

