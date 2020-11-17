from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie
from .models import MovieGenre
from .models import MovieRatings
from .models import Directors

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
        genres = MovieGenre.objects.filter(movie_id=movid)
        ratings = MovieRatings.objects.get(movie_id=movid)
        return render(request, "recommender/movie.html", {'movie' : movie, 'genres' : genres, 'ratings' : ratings})
    else:
        return render(request, "recommender/index.html")

def similar(request):
    org_movie = Movie.objects.get(movie_id=request.GET.get('movie_id'))
    #genres = [movieGenre.genre for movieGenre in MovieGenre.objects.filter(movie_id=org_movie)]
    #org_title_words = [''.join(c for c in word.lower() if c.isalnum()) for word in org_movie.title.split()]

    # if word is contained in title
    #titleregexp = '(' + r'\b|\b'.join(word for word in org_title_words) + ')'
    #movies = Movie.objects.filter(title__regex=titleregexp).all()

    directorid = Directors.objects.get(movie_id=org_movie)
    director_movies = [director.movie_id for director in Directors.objects.filter(director_id=directorid.director_id)]

    return render(request, "recommender/similar.html", {'movies' : director_movies})