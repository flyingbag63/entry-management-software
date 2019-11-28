from django.http import HttpResponse
from django.shortcuts import render
from products.models import Entry
# Create your views here.

def index(request):
	return render(request,"index.html")
