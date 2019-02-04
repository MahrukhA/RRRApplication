from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'listings/viewlistings.html')


def listing(request):
    return render(request, 'listings/listing.html')
