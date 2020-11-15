from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

# Create your views here.
def index(request):
    return render(request, "recommender/index.html")

def search(request):
    if request.GET.get('title'):
        movietitle = request.GET.get('title')
        movieslist = Movie.objects.filter(title__contains=movietitle).all()[:10]
        return render(request, "recommender/search.html", {'movieslist' : movieslist})
    else:
        return render(request, "recommender/index.html")