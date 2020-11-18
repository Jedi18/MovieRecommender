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
    search_type = request.GET.get('search_type')

    print(search_type)
        
    if search_type == 'title':
        return render(request, "recommender/similar.html", {'movies' : getMoviesContainingSameWordsInTitle(org_movie)})
    elif search_type == 'director':
        return render(request, "recommender/similar.html", {'movies' : getMoviesBySameDirector(org_movie)})
    elif search_type == 'genre':
        return render(request, "recommender/similar.html", {'movies' : getMoviesByGenre(org_movie)})
    elif search_type == 'year':
        return render(request, "recommender/similar.html", {'movies' : getMoviesInSameYear(org_movie)})
    else:
        return render(request, "recommender/index.html")

# movies directed by the same director
def getMoviesBySameDirector(org_movie):
    directorid = Directors.objects.get(movie_id=org_movie)
    director_movies = [director.movie_id for director in Directors.objects.filter(director_id=directorid.director_id)]
    return director_movies

# word contained in title and of the same genre
def getMoviesContainingSameWordsInTitle(org_movie):
    common_words = ['the', 'on', 'at', 'in', 'of', 'is', 'a']
    org_title_words = [''.join(c for c in word.lower() if c.isalnum()) for word in org_movie.title.split() if word.lower() not in common_words]
    genres = [movieGenre.genre for movieGenre in MovieGenre.objects.filter(movie_id=org_movie)]

    titleregexp = r'(\b' + r'\b|\b'.join((word + r'\b|\b' + word.title()) for word in org_title_words) + r'\b)'
    movies = {movieGenre.movie_id for movieGenre in MovieGenre.objects.filter(movie_id__title__regex=titleregexp).filter(genre__in=genres)}
    return list(movies)

# popular movies of the same genres
def getMoviesByGenre(org_movie):
    genres = [movieGenre.genre for movieGenre in MovieGenre.objects.filter(movie_id=org_movie)]
    top_rated_movies = [movieRating.movie_id for movieRating in MovieRatings.objects.order_by('-num_votes')[:50]]

    result = []
    for mov in top_rated_movies:
        movGenres = MovieGenre.objects.filter(movie_id=mov)
        for movGenre in movGenres:
            if movGenre.genre in genres:
                result.append(mov)
                break

    return result

# movies released in same year of the same genre
def getMoviesInSameYear(org_movie):
    genres = [movieGenre.genre for movieGenre in MovieGenre.objects.filter(movie_id=org_movie)]
    movies_in_same_year = Movie.objects.filter(year=org_movie.year)[:100]

    result = []
    for mov in movies_in_same_year:
        movGenres = MovieGenre.objects.filter(movie_id=mov)
        for movGenre in movGenres:
            if movGenre.genre in genres:
                result.append(mov)
                break

    return result