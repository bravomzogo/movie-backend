from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Genre, TVShow, Season, BongoMovie, LiveStream
from .serializers import MovieSerializer, GenreSerializer, SeasonSerializer, TVShowSerializer, BongoMovieSerializer, LiveStreamSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q

class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genres', 'is_featured', 'is_new', 'is_4k']
    search_fields = ['title', 'director', 'cast']

class FeaturedMoviesAPIView(generics.ListAPIView):
    queryset = Movie.objects.filter(is_featured=True)
    serializer_class = MovieSerializer

class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

class TVShowListAPIView(generics.ListAPIView):
    queryset = TVShow.objects.all().prefetch_related('genres', 'seasons')
    serializer_class = TVShowSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genres', 'is_featured', 'is_new', 'is_trending']
    search_fields = ['title', 'director', 'cast']

class FeaturedTVShowsAPIView(generics.ListAPIView):
    queryset = TVShow.objects.filter(is_featured=True).prefetch_related('genres', 'seasons')
    serializer_class = TVShowSerializer

class TrendingTVShowsAPIView(generics.ListAPIView):
    queryset = TVShow.objects.filter(is_trending=True).prefetch_related('genres', 'seasons')
    serializer_class = TVShowSerializer

class TVShowDetailAPIView(generics.RetrieveAPIView):
    queryset = TVShow.objects.all().prefetch_related('genres', 'seasons')
    serializer_class = TVShowSerializer
    lookup_field = 'id'

class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class SeasonDetailAPIView(generics.RetrieveAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    lookup_field = 'id'

class BongoMovieListAPIView(generics.ListAPIView):
    queryset = BongoMovie.objects.all()
    serializer_class = BongoMovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genres', 'is_featured', 'is_new', 'is_4k']
    search_fields = ['title', 'director', 'cast']

class FeaturedBongoMoviesAPIView(generics.ListAPIView):
    queryset = BongoMovie.objects.filter(is_featured=True)
    serializer_class = BongoMovieSerializer

class BongoMovieDetailAPIView(generics.RetrieveAPIView):
    queryset = BongoMovie.objects.all()
    serializer_class = BongoMovieSerializer
    lookup_field = 'id'

class LiveStreamListAPIView(generics.ListAPIView):
    queryset = LiveStream.objects.all().prefetch_related('genres')
    serializer_class = LiveStreamSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genres', 'is_featured', 'is_live']
    search_fields = ['title', 'description']

class FeaturedLiveStreamAPIView(generics.ListAPIView):
    queryset = LiveStream.objects.filter(is_featured=True).prefetch_related('genres')
    serializer_class = LiveStreamSerializer

class LiveStreamDetailAPIView(generics.RetrieveAPIView):
    queryset = LiveStream.objects.all().prefetch_related('genres')
    serializer_class = LiveStreamSerializer
    lookup_field = 'id'

class SearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'results': []}, status=status.HTTP_200_OK)

        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        )
        movie_serializer = MovieSerializer(movies, many=True, context={'request': request})

        tvshows = TVShow.objects.filter(
            Q(title__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        ).prefetch_related('genres', 'seasons')
        tvshow_serializer = TVShowSerializer(tvshows, many=True, context={'request': request})

        bongomovies = BongoMovie.objects.filter(
            Q(title__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        )
        bongomovie_serializer = BongoMovieSerializer(bongomovies, many=True, context={'request': request})

        livestreams = LiveStream.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).prefetch_related('genres')
        livestream_serializer = LiveStreamSerializer(livestreams, many=True, context={'request': request})

        results = [
            {'id': item['id'], 'title': item['title'], 'poster': item['poster'], 'type': 'movie'}
            for item in movie_serializer.data
        ] + [
            {'id': item['id'], 'title': item['title'], 'poster': item['poster'], 'type': 'tv'}
            for item in tvshow_serializer.data
        ] + [
            {'id': item['id'], 'title': item['title'], 'poster': item['poster'], 'type': 'bongomovie'}
            for item in bongomovie_serializer.data
        ] + [
            {'id': item['id'], 'title': item['title'], 'poster': item['poster'], 'type': 'livestream'}
            for item in livestream_serializer.data
        ]

        return Response({'results': results}, status=status.HTTP_200_OK)