from django.shortcuts import render
from django.http import HttpResponse
from .models import Contact


def index(request):
    return HttpResponse('Oh hello there')

def file_load(request):
    return HttpResponse('Going to load the file allllright')
