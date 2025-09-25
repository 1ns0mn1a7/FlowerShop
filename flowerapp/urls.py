from django.urls import path
from .views import create_consultation

urlpatterns = [
    path('consultations/create/', create_consultation, name='consultation-create'),
]