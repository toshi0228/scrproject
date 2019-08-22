
from django.urls import path, include
from .views import index, rev, finish, ja

urlpatterns = [
    path("", index),
    path('index/',rev, name='index'),
    path('finish/',finish, name='finish'),
    path("jafinish/", ja, name='ja'),
]
