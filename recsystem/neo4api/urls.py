from django.conf.urls import url
from neo4api.views import *
from django.urls import path

urlpatterns = [
    path('getAllPersons',getAllPersons),
]