from django.urls import path, include
from .views import index, rev, finish, ja, jaex, rt, rtsa, rtnum, janum

urlpatterns = [
    path("", index),
    path('index/',rev, name='index'),
    path('finish/',finish, name='finish'),
    path("jafinish/", ja, name='ja'),
    path("jaexfinish/", jaex, name='jaex'),
    path("rt/", rt, name='rt'),
    path("rtsa/", rtsa, name="rtsa"),
    path("rtnum/", rtnum, name="rtnum"),
    path('janum/', janum, name='janum'),
]
