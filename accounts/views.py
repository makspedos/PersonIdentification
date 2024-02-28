from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress



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

class AccountEmail(generic.ListView):
    template_name = "account/email.html"
    context_object_name = 'email_addresses'

    def get_success_url(self):
        return reverse_lazy('accounts:profile')
    def get_queryset(self):
        query = EmailAddress.objects.filter(user=self.request.user, primary=False)
        return query
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        if 'email-add' in request.POST:
            new_email = request.POST.get('email')
            if EmailAddress.objects.filter(email=new_email):
                messages.error(request, 'Пошта вже зайнята')
                return HttpResponseRedirect(reverse_lazy('accounts:email'))

            self.changing_primary(request, new_email)
            EmailAddress.objects.create(user=self.request.user, email=new_email, primary=True, verified=True)


        if 'email-primary' in request.POST:
            email = request.POST.get('email')

            self.changing_primary(request, email)
            email_obj = EmailAddress.objects.get(email=email)
            email_obj.primary = True
            email_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def changing_primary(self, request, new_email):
        old_email = self.request.user.email
        old_email_obj = EmailAddress.objects.get(email=old_email)
        old_email_obj.primary = False
        old_email_obj.save()
        self.request.user.email = new_email
        self.request.user.save()