from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Contact
import csv


def index(request):
    return HttpResponse('Oh hello there')


def file_load(request):
    try:
        csv_data = open('test-data.csv', 'rU')
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
    number = conform_number(number)
    if len(number) > 15:
        return False
    return True


def conform_number(number):
    number = str(number)
    chars_to_remove = ['-', ',', '.', ' ', '(', ')']
    return number.translate(None, ''.join(chars_to_remove))
