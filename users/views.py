from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView
from .forms import AuthForm, RegistrationForm, ProfileForm
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin


class MainPageView(TemplateView):
    """ Show main page """
    template_name = 'app_users/base_template.html'


class AuthFormView(LoginView):
    """ Show authentication form """
    authentication_form = AuthForm
    template_name = 'app_users/login.html'


def registration_form_view(request):
    """ Show registration form """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            Profile.objects.create(user=user)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('main'))
    else:
        form = RegistrationForm()
    return render(request, 'app_users/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'app_users/profile.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'app_users/profile-edit.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        profile = self.object
        user = profile.user
        first_name = user.first_name
        last_name = user.last_name
        form = ProfileForm(instance=profile, initial={'first_name': first_name,
                                                      'last_name': last_name})
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context

    def form_valid(self, form):
        profile = self.object
        user = profile.user
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()
        return super().form_valid(form)
