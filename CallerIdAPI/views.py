from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest
from .models import Contact
import csv


def index(request):
    return HttpResponse('Oh hello there')


def query(request):
    if request.method == 'POST':
        return True
    elif request.method == 'GET':
        return HttpResponse('Made it')
    else:
        return HttpResponseBadRequest('Method not supported')

def file_load(request):
    """
    This function loads a file with the specified name. The file name is hard-coded to interview-callerid-data.csv and
    must be placed in the project root
    """
    try:
        csv_data = open('interview-callerid-data.csv', 'rU')
        reader = csv.reader(csv_data)
        count = 0
        for row in reader:
            conformed_number = conform_number(row[0])
            if validate_number(conformed_number):
                new_contact = Contact()
                new_contact.number = conformed_number
                new_contact.context = row[1]
                new_contact.name = row[2]
                new_contact.save()
                count += 1
    except Exception, e:
        raise Http404(str(e))
    return HttpResponse('Processed records: ' + str(count))


def validate_number(number):
    """
    Very simple length validation, but exists as its own function to scale/add additional validation as needed
    """
    number = conform_number(number)
    if len(number) > 15:
        return False
    return True


def conform_number(number):
    """
    Filters the file input to remove unneeded/unwanted characters. Also casts the input into a string
    """
    number = str(number)
    chars_to_remove = ['-', ',', '.', ' ', '(', ')']
    return number.translate(None, ''.join(chars_to_remove))
