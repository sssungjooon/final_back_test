import requests

def get_movie_Data() :
    result = []
    TMDB_API_KEY = "b490976b819d28133d6448f4ef4ef0d8"

    for i in range(1, 2):
        request_url_up = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko"

        movies = requests.get(request_url_up).json()

        for movie in movies["results"] :
            data = {}
            data["pk"] = movie["id"]
            data["model"] = "movies.movie"
            movie_key = movie["id"]
            fields = {}
            fields["popularity"] = movie["popularity"]
            fields["overview"] = movie["overview"]
            fields["title"] = movie["title"]
            fields["release_date"] = movie["release_date"]
            fields["vote_average"] = movie["vote_average"]
            fields["genres_ids"] = movie["genres_ids"]
            fields["poster_path"] = movie["poster_path"]
            # video_path 가져오기
            request_videos = f"https://api.themoviedb.org/3/movie/{movie_key}/videos?api_key={TMDB_API_KEY}&append_to_response=videos&language=ko"
            videos = requests.get(request_videos).json()
            fields["video_path"] = videos["results"][0].get("key")
            result.append(data, fields)
    return result

with open('../221119_json_make/movie_list.json', 'w', encoding="UTF-8") as f :
    json.dump(get_movie_Data(), f, ensure_ascii=False, indent=2)