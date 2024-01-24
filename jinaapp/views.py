from django.shortcuts import render

# Create your views here.
# yourappname/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'jinaapp/index.html')

#update view
