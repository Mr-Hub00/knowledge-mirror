import os
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from core.models import DocumentStamp

def home(request):
    return HttpResponse("IAmHub engine online — UI coming last.")

@csrf_exempt
def storacha_health(request):
    return JsonResponse({"storacha": "ok"})

def health(request):
    return JsonResponse({"status": "ok"})

def index(request):
    return render(request, "index.html")