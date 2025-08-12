from rest_framework import serializers
from .models import Genre, Movie, TVShow, Season, Episode, DownloadLink, BongoMovie, LiveStream

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class DownloadLinkSerializer(serializers.ModelSerializer):
    quality_display = serializers.CharField(source='get_quality_display', read_only=True)
    
    class Meta:
        model = DownloadLink
        fields = ['id', 'quality', 'quality_display', 'url', 'source']

class EpisodeSerializer(serializers.ModelSerializer):
    download_links = DownloadLinkSerializer(many=True, read_only=True)
    
    class Meta:
        model = Episode
        fields = ['id', 'episode_number', 'title', 'download_links']

class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Season
        fields = ['id', 'season_number', 'episode_count', 'episodes']

class TVShowSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    seasons = SeasonSerializer(many=True, read_only=True)
    poster = serializers.SerializerMethodField()
    backdrop = serializers.SerializerMethodField()
    
    class Meta:
        model = TVShow
        fields = [
            'id', 'title', 'description', 'release_year', 'rating', 'poster', 'backdrop',
            'trailer_url', 'genres', 'seasons', 'is_featured', 'is_new', 'is_trending',
            'director', 'cast', 'created_at'
        ]
    
    def get_poster(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return obj.poster_url
    
    def get_backdrop(self, obj):
        if obj.backdrop_image:
            return self.context['request'].build_absolute_uri(obj.backdrop_image.url)
        return obj.backdrop_url

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    poster = serializers.SerializerMethodField()
    backdrop = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_year', 'rating', 'poster', 'backdrop',
            'trailer_url', 'download_url', 'duration', 'genres', 'is_4k', 'is_new',
            'is_featured', 'director', 'cast', 'created_at'
        ]
    
    def get_poster(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return obj.poster_url
    
    def get_backdrop(self, obj):
        if obj.backdrop_image:
            return self.context['request'].build_absolute_uri(obj.backdrop_image.url)
        return obj.backdrop_url

class BongoMovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    poster = serializers.SerializerMethodField()
    backdrop = serializers.SerializerMethodField()
    
    class Meta:
        model = BongoMovie
        fields = [
            'id', 'title', 'description', 'release_year', 'rating', 'poster', 'backdrop',
            'trailer_url', 'download_url', 'duration', 'genres', 'is_4k', 'is_new',
            'is_featured', 'director', 'cast', 'created_at'
        ]
    
    def get_poster(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return obj.poster_url
    
    def get_backdrop(self, obj):
        if obj.backdrop_image:
            return self.context['request'].build_absolute_uri(obj.backdrop_image.url)
        return obj.backdrop_url

class LiveStreamSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    poster = serializers.SerializerMethodField()
    backdrop = serializers.SerializerMethodField()
    video_file = serializers.SerializerMethodField()
    
    class Meta:
        model = LiveStream
        fields = [
            'id', 'title', 'description', 'video_file', 'poster', 'backdrop',
            'genres', 'is_live', 'is_featured', 'created_at'
        ]
    
    def get_poster(self, obj):
        if obj.poster_image:
            return self.context['request'].build_absolute_uri(obj.poster_image.url)
        return obj.poster_url
    
    def get_backdrop(self, obj):
        if obj.backdrop_image:
            return self.context['request'].build_absolute_uri(obj.backdrop_image.url)
        return obj.backdrop_url
    
    def get_video_file(self, obj):
        if obj.video_file:
            return self.context['request'].build_absolute_uri(obj.video_file.url)
        return None