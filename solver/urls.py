from django.urls import path, include
from .views import InputStream, acknowledge, solve, reset

urlpatterns = [
    path('InputStream/<str:face>', InputStream),
    path('acknowledge/<str:face>', acknowledge),
    path('solve/', solve),
    path('reset/', reset)
]
