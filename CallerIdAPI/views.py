from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Contact
import json
import csv


def index(request):
    return HttpResponse('Oh hello there')


def query(request):
    if request.method == 'GET':
        request_number = request.GET.get('number', '')
        request_number = conform_number(request_number)
        if not validate_number(request_number):
            return HttpResponseBadRequest('Invalid query - number is not E.164 format compliant')
        located_contacts = Contact.objects.filter(number=request_number)
        if located_contacts:
            outgoing_contacts = []
            for contact in located_contacts:
                outgoing_contact = {}
                outgoing_contact['name'] = contact.name
                outgoing_contact['number'] = contact.number
                outgoing_contact['context'] = contact.context
                outgoing_contacts.append(outgoing_contact)
            return HttpResponse(json.dumps({"results": outgoing_contacts}))
        else:
            raise Http404('No contacts found')
    else:
        return HttpResponseBadRequest('Method not supported')

@csrf_exempt
def number(request):
    """
    Persists a new Contact based on a POST JSON body with name, number, and context. If an existing number/context
    is already found, just return an OK to maintain a semblance of idempotence
    """
    if request.method == 'POST':
        # Extract post body and convert to array. Also validate the post body
        post_body = json.loads(request.body)
        validate_post(post_body)
        if not validate_post(post_body):
            return HttpResponseBadRequest('Bad request body. Please ensure name, number, and context are included')

        # Look for a matching number/context pair. If one is found, just return an OK. Otherwise, persist.
        matching_contact = Contact.objects.filter(number=post_body['number'], context=post_body['context'])
        if matching_contact:
            return HttpResponse(status=200)
        else:
            post_number = conform_number(post_body['number'])
            if not validate_number(post_number):
                return HttpResponseBadRequest('Invalid query - number is not E.164 format compliant')
            new_contact = Contact()
            new_contact.name = post_body['name']
            new_contact.number = post_number
            new_contact.context = post_body['context']
            new_contact.save()

        return HttpResponse(status=200)
    else:
        return HttpResponseBadRequest('Method not supported')


def validate_post(post_body):
    """
    Validates a post request by ensuring that every component is present
    """
    valid = True
    if 'number' not in post_body:
        valid = False
    elif 'name' not in post_body:
        valid = False
    elif 'context' not in post_body:
        valid = False

    return valid


def file_load(request):
    """
    This function loads a file with the specified name. The file name is hard-coded to interview-callerid-data.csv and
    must be placed in the project root. Depending on the file size, this could take awhile...
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
