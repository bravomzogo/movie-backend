from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from movies.views import (
    FeaturedTVShowsAPIView, MovieListAPIView, MovieDetailAPIView, FeaturedMoviesAPIView,
    TVShowDetailAPIView, TVShowListAPIView, TrendingTVShowsAPIView, GenreListAPIView,
    SearchAPIView, BongoMovieListAPIView, FeaturedBongoMoviesAPIView, BongoMovieDetailAPIView,
    LiveStreamListAPIView, FeaturedLiveStreamAPIView, LiveStreamDetailAPIView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('contact.urls')),
    path('api/movies/', MovieListAPIView.as_view(), name='movie-list'),
    path('api/movies/featured/', FeaturedMoviesAPIView.as_view(), name='featured-movies'),
    path('api/movies/<int:id>/', MovieDetailAPIView.as_view(), name='movie-detail'),
    path('api/tvshows/', TVShowListAPIView.as_view(), name='tvshow-list'),
    path('api/tvshows/featured/', FeaturedTVShowsAPIView.as_view(), name='featured-tvshows'),
    path('api/tvshows/trending/', TrendingTVShowsAPIView.as_view(), name='trending-tvshows'),
    path('api/tvshows/<int:id>/', TVShowDetailAPIView.as_view(), name='tvshow-detail'),
    path('api/genres/', GenreListAPIView.as_view(), name='genre-list'),
    path('api/bongomovies/', BongoMovieListAPIView.as_view(), name='bongomovie-list'),
    path('api/bongomovies/featured/', FeaturedBongoMoviesAPIView.as_view(), name='featured-bongomovies'),
    path('api/bongomovies/<int:id>/', BongoMovieDetailAPIView.as_view(), name='bongomovie-detail'),
    path('api/livestreams/', LiveStreamListAPIView.as_view(), name='livestream-list'),
    path('api/livestreams/featured/', FeaturedLiveStreamAPIView.as_view(), name='featured-livestreams'),
    path('api/livestreams/<int:id>/', LiveStreamDetailAPIView.as_view(), name='livestream-detail'),
    path('api/search/', SearchAPIView.as_view(), name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)