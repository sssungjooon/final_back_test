from rest_framework import serializers

from .models import Genre
from .models import Movie
# from .models import Tournament

class GenreSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Genre
        fields = "__all__"

class GenreSerializerId(serializers.ModelSerializer): # 데이터 넣을 때

    class Meta : 
        model = Genre
        fields = ('id', )



class MovieSerializer(serializers.ModelSerializer): # 데이터 넣을 때
   
    class Meta : 
        model = Movie
        fields="__all__"

class MovieDetailSerializer(serializers.ModelSerializer): # 영화상세
    genres = GenreSerializer(many=True, read_only=True)

    class Meta : 
        model = Movie
        fields = "__all__"
    
# 해당 월에 맞는 장르 뽑아내기
class MonthGenreMatchSerializer(serializers.ModelSerializer):
    movies_by_genre = serializers.SerializerMethodField()

    class Meta :
        model = Genre
        fields = ('id','name','movies_by_genre',)

    def get_movies_by_genre(self, obj):
        movies = Movie.objects.all().order_by('-release_date')
        return movies.filter(genres_ids=obj.id).values()

# class TournamentSerializer(serializers.ModelSerializer): 
#     class Meta : 
#         model = Tournament
#         fields = "__all__"


