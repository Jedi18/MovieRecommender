from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search', views.search, name='search'),
    path('movie', views.movie, name='movie'),
    path('similar', views.similar, name='similar')
]