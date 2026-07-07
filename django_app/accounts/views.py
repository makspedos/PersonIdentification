from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomPasswordChangeForm, CustomUserChangeForm, CustomUserCreationForm
from web.models import Identification, ImageFaces


class SignUpPageView(generic.CreateView):
    """Create a new user account with the project signup form."""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("account_login")
    template_name = "account/signup.html"


class AccountProfileView(generic.ListView):
    """Render the current user's profile page."""

    template_name = "account/profile.html"
    model = get_user_model()

    def get_context_data(self, **kwargs):
        """Add the authenticated user to the template context."""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class AccountChangePassword(generic.FormView):
    """Handle password changes from the account settings page."""

    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("accounts:profile")
    template_name = "account/password_change.html"

    def post(self, request):
        """Validate and save the current user's new password."""
        form = CustomPasswordChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
        return render(request, self.template_name, {"form": form})


class AccountChangeUsername(generic.FormView):
    """Handle username changes from the account settings page."""

    form_class = CustomUserChangeForm
    template_name = "account/username_change.html"
    success_url = reverse_lazy("accounts:profile")

    def post(self, request):
        """Validate and save the current user's new username."""
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
        return render(request, self.template_name, {"form": form})


class AccountEmail(generic.ListView):
    """List, add, promote, and delete account email addresses."""

    template_name = "account/email.html"
    context_object_name = "email_addresses"

    def get_success_url(self):
        """Return the profile page after email changes complete."""
        return reverse_lazy("accounts:profile")

    def get_queryset(self):
        """Return non-primary email addresses for the current user."""
        return EmailAddress.objects.filter(user=self.request.user, primary=False)

    def get_context_data(self, **kwargs):
        """Add the authenticated user to the template context."""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        """Apply the requested email-management action."""
        if "email-add" in request.POST:
            new_email = request.POST.get("email")
            if EmailAddress.objects.filter(email=new_email):
                messages.error(request, "Email is already in use")
                return HttpResponseRedirect(reverse_lazy("accounts:email"))
            if new_email == "":
                messages.error(request, "Enter an email address")
                return HttpResponseRedirect(reverse_lazy("accounts:email"))
            self.changing_primary(new_email)
            EmailAddress.objects.create(user=self.request.user, email=new_email, primary=True, verified=True)
        if "email-primary" in request.POST:
            email = request.POST.get("email")
            self.changing_primary(email)
            email_obj = EmailAddress.objects.get(email=email)
            email_obj.primary = True
            email_obj.save()
        if "email-delete" in request.POST:
            email = request.POST.get("email")
            EmailAddress.objects.get(email=email).delete()
        return HttpResponseRedirect(self.get_success_url())

    def changing_primary(self, new_email):
        """Mark the current primary email as secondary and update the user."""
        old_email = self.request.user.email
        old_email_obj = EmailAddress.objects.get(email=old_email)
        old_email_obj.primary = False
        old_email_obj.save()
        self.request.user.email = new_email
        self.request.user.save()


class AccountSavedResults(generic.ListView):
    """Render saved images and their associated face-analysis results."""

    template_name = "account/results_page.html"
    model = get_user_model()

    def get_context_data(self, **kwargs):
        """Add the authenticated user to the template context."""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        images = ImageFaces.objects.filter(user=self.request.user)
        context["dict_results"] = {
            image: Identification.objects.filter(image_face=image)
            for image in images
        }
        context["col_list"] = ["Face", "Age", "Gender", "Emotion"]
        return context