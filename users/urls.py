from django.urls import path
from .views import MainPageView, AuthFormView, registration_form_view, ProfileView, ProfileEditView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    #path('', MainPageView.as_view(), name='main'),
    path('login/', AuthFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', registration_form_view, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile-edit'),
]
