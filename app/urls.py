from django.urls import path
from .views import upload_csv, get_movies

urlpatterns = [
    path('upload_csv/', upload_csv, name='upload_csv'),
    path('get_movies/', get_movies, name='get_movies'),
]