import csv
from recommender.models import MovieGenre
from recommender.models import Movie

with open("title.basics.tsv/data.tsv", encoding="utf8") as data_file:
    data_reader = csv.reader(data_file, delimiter="\t")

    for row in data_reader:
        if row[1] == "movie":
            if row[0] == '\\N':
                continue
            movieId = row[0]

            if row[8] == '\\N':
                continue

            movieGenres = row[8].split(',')

            for genre in movieGenres:
                movGenre = MovieGenre(movie_id=Movie.objects.get(movie_id=movieId), genre=genre)
                movGenre.save()