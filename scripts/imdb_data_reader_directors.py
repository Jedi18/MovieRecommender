import csv
from recommender.models import Movie
from recommender.models import Directors

with open("title.crew.tsv/data.tsv", encoding="utf8") as data_file:
    data_reader = csv.reader(data_file, delimiter="\t")

    for row in data_reader:
        try:
            mov = Movie.objects.get(movie_id=row[0])
            if row[1] == '\\N':
                continue
            
            director = Directors(movie_id=mov, director_id=row[1])
            director.save()
        except Movie.DoesNotExist:
            pass