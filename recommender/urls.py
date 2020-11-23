from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search', views.search, name='search'),
    path('movie', views.movie, name='movie'),
    path('similar', views.similar, name='similar'),
    path('addmovie', views.addmovie, name='addmovie'),
    path('deletemovie', views.deletemovie, name='deletemovie'),
    path('updatemovie', views.updatemovie, name='updatemovie'),
    path('success', views.success, name='success')
]