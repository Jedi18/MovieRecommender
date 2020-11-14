import csv
from recommender.models import Movie

with open("title.basics.tsv/data.tsv", encoding="utf8") as data_file:
    data_reader = csv.reader(data_file, delimiter="\t")

    for row in data_reader:
        if row[1] == "movie":
            if row[0] == '\\N':
                continue
            
            if row[2] == '\\N':
                continue

            if row[4] == '\\N':
                continue

            movieId = row[0]
            movieTitle = row[2]
            movieAdult = row[4]
            movieYear = row[5]

            if movieYear == '\\N':
                movieYear = 1999

            if row[7] == '\\N':
                movieRuntime = None
            else:
                movieRuntime = row[7]
        
            mov = Movie(movie_id=movieId, title=movieTitle, is_adult=movieAdult, year=movieYear, runtime=movieYear)
            mov.save()