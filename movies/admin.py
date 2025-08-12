from django.contrib import admin
from .models import Movie, Genre, TVShow, Season, Episode, DownloadLink, BongoMovie, LiveStream

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(TVShow)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(DownloadLink)
admin.site.register(BongoMovie)
admin.site.register(LiveStream)