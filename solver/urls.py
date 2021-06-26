from django.urls import path, include
from .views import InputStream, acknowledge, solve, reset

urlpatterns = [
    path('InputStream/', InputStream),
    path('acknowledge/', acknowledge),
    path('solve/', solve),
    path('reset/', reset)
]
