from django.urls import path
from .views import signup

app_name = 'registro'

urlpatterns = [
    path('', signup, name='registro'),
]