import csv
from recommender.models import Movie
from recommender.models import MovieRatings

with open("title.ratings.tsv/data.tsv", encoding="utf8") as data_file:
    data_reader = csv.reader(data_file, delimiter="\t")

    for row in data_reader:
        try:
            mov = Movie.objects.get(movie_id=row[0])
            movRating = MovieRatings(movie_id=mov, average_rating=row[1], num_votes=row[2])
            movRating.save()
        except Movie.DoesNotExist:
            pass