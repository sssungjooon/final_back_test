from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

from .models import Movie, Genre
from .serializers import MovieSerializer, MovieDetailSerializer
from django.shortcuts import render

# import datetime
# start_date = datetime.date(2005, 1, 1)
# end_date = datetime.date(2005, 3, 31)

# Create your views here.
@api_view(['GET'])
def main(request) :
    latest_movies = Movie.objects.order_by('-release_date').prefetch_related('genres')[:20]
    highscore_movies = Movie.objects.order_by('-vote_average').prefetch_related('genres')[:20]
    # date_movies = Movie.objects.
    # like_movies = Movie.objects.order_by('-vote_count').prefetch_related('genres')[:20]

    latest_serializer = MovieSerializer(data=latest_movies, many=True)
    highscore_serializer = MovieSerializer(data=highscore_movies, many=True)
    # like_serializer = MovieSerializer(data=like_movies, many=True)

    print(latest_serializer.is_valid() , highscore_serializer.is_valid())
    # like_serializer.is_valid()
    
    context={
        'latest_movies' : latest_serializer.data,
        'highscore_movies' : highscore_serializer.data,
        # 'like_movies' : like_serializer.data,
    }
    return Response(context)

@api_view(['GET'])
def movie_detail(request, movie_pk) :
    movie = Movie.objects.get(pk=movie_pk)
    movie_list = [movie]
    # serializer = MovieDetailSerializer(data = movie)
    serializer = MovieDetailSerializer(data = movie_list, many=True)

    # 한영화의 genres에 포함된 genre를 포함하는 genres를 가지고 있는 영화들을 찾고 싶다. - 해결
    
    genres = movie.genres.all().values_list('id', flat=True) # 영화의 모든 genre를 id 객체로 가져오기
    movies_same_genre = Movie.objects.filter(genres__id__in=genres).prefetch_related('genres').distinct().order_by('-vote_count')[:20]

    # recommended_movies = Movie.objects.filter(genres = movie.genres.all())[:10]
    same_genre_serializer = MovieSerializer(data = movies_same_genre, many=True)
    print(serializer.is_valid(), same_genre_serializer.is_valid())
    context = {
        "movie" : serializer.data, 
        "same_genres" : same_genre_serializer.data,
    }

    # movieSerializer = MovieSerializer(data = recommended_movies, many=True)
    return Response(context)

@api_view(['GET'])
def mypageMovie(request, username) :
    person = get_object_or_404(get_user_model(), username=username)
    winMovies = Movie.objects.filter(tournament__user=person).order_by('-tournament__created_at') # OneToMany 접근
    # likeMovies = Review.objects.filter(user=person).filter(liked=True).order_by('-created_at')
    likeMovies = Movie.objects.filter(review__user=person).distinct()

    winMoviesSerializer = MovieSerializer(data = winMovies, many=True)
    likeMoviesSerializer = MovieSerializer(data= likeMovies, many=True)

    print(winMoviesSerializer.is_valid(), likeMoviesSerializer.is_valid())
    context = {
        'winMovies' : winMoviesSerializer.data, 
        'likeMovies' : likeMoviesSerializer.data
    }
    return Response(context)