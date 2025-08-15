from django.http import HttpResponse

def home(request):
    return HttpResponse("IAmHub engine online — UI coming last.")