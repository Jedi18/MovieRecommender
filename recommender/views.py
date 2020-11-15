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

def movie(request):
    if request.GET.get('movie_id'):
        movid = request.GET.get('movie_id')
        movie = Movie.objects.get(movie_id=movid)
        return render(request, "recommender/movie.html", {'movie' : movie})
    else:
        return render(request, "recommender/index.html")

def similar(request):
    print(request.GET.get('movie_id'))
    return render(request, "recommender/similar.html")