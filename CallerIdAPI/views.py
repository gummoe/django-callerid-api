from django.shortcuts import render
from django.http import HttpResponse
from .models import Contact


def file_load():
    return HttpResponse('Oh hello there')
