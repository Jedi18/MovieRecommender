import random

from django.shortcuts import render
from django.shortcuts import redirect
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
        try:
            ratings = MovieRatings.objects.get(movie_id=movid)
        except MovieRatings.DoesNotExist:
            ratings = None
        return render(request, "recommender/movie.html", {'movie' : movie, 'genres' : genres, 'ratings' : ratings})
    else:
        return render(request, "recommender/index.html")

def similar(request):
    org_movie = Movie.objects.get(movie_id=request.GET.get('movie_id'))
    search_type = request.GET.get('search_type')

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

def addmovie(request):
    if request.method == "POST":
        newtitle = request.POST.get('title')
        if request.POST.get('year') == 'on':
            newisadult = True
        else:
            newisadult = False
        newrandomid = "custom" + str(random.randint(0,100000))
        newyear = request.POST.get('year')
        newgenres = request.POST.getlist('genres')
        newmovie = Movie(movie_id=newrandomid, title=newtitle, is_adult=newisadult, year=newyear, runtime=newyear)
        newmovie.save()

        for genre in newgenres:
            newgenre = MovieGenre(movie_id=newmovie, genre=genre)
            newgenre.save()

        return render(request, "recommender/index.html")
    else:
        genres_list = [movGenre['genre'] for movGenre in MovieGenre.objects.order_by().values('genre').distinct()]
        return render(request, "recommender/addmovie.html", {'genres' : genres_list})

def updatemovie(request):
    if request.method == "POST":
        newtitle = request.POST.get('title')
        if request.POST.get('year') == 'on':
            newisadult = True
        else:
            newisadult = False
        newyear = request.POST.get('year')

        movie = Movie.objects.get(movie_id=request.POST.get('movie_id'))
        movie.title = newtitle
        movie.is_adult = newisadult
        movie.year = newyear
        movie.save()

        return redirect('success')
    else:
        movid = request.GET.get('movie_id')
        movie = Movie.objects.get(movie_id=movid)
        return render(request, "recommender/updatemovie.html", {'movie' : movie})

def deletemovie(request):
    if request.GET.get('movie_id'):
        movid = request.GET.get('movie_id')
        try:
            movie = Movie.objects.get(movie_id=movid)
            genres = MovieGenre.objects.filter(movie_id=movid)
            movie.delete()

            for genre in genres:
                genre.delete()
        except:
            print("Movie not found")

    return redirect('success')

def success(request):
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