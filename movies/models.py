from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.PositiveIntegerField()
    rating = models.FloatField()
    poster_image = models.ImageField(upload_to='posters/', null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    backdrop_image = models.ImageField(upload_to='backdrops/', null=True, blank=True)
    backdrop_url = models.URLField(null=True, blank=True)
    trailer_url = models.CharField(max_length=100, help_text="YouTube video ID", null=True, blank=True)
    download_url = models.URLField(null=True, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)
    director = models.CharField(max_length=200, blank=True)
    cast = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre)
    is_4k = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) 
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    def get_poster(self):
        return self.poster_image.url if self.poster_image else self.poster_url

    def get_backdrop(self):
        return self.backdrop_image.url if self.backdrop_image else self.backdrop_url

class TVShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.PositiveIntegerField()
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        null=True,
        blank=True
    )
    poster_image = models.ImageField(upload_to='tv_posters/', null=True, blank=True)
    backdrop_image = models.ImageField(upload_to='tv_backdrops/', null=True, blank=True)
    poster_url = models.URLField(blank=True, null=True)
    backdrop_url = models.URLField(blank=True, null=True)
    trailer_url = models.CharField(max_length=512, blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    director = models.CharField(max_length=255, blank=True, null=True)
    cast = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.release_year})"

class Season(models.Model):
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    episode_count = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Total number of episodes in this season"
    )
    
    class Meta:
        unique_together = ('tv_show', 'season_number')
        ordering = ['season_number']
        
    def __str__(self):
        return f"{self.tv_show.title} - Season {self.season_number}"

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        unique_together = ('season', 'episode_number')
        ordering = ['episode_number']
        
    def __str__(self):
        return f"S{self.season.season_number}E{self.episode_number} - {self.title or 'Untitled'}"

class DownloadLink(models.Model):
    QUALITY_CHOICES = [
        ('HD', 'High Definition'),
        ('4K', 'Ultra HD'),
        ('SD', 'Standard Definition'),
    ]
    
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='download_links')
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES)
    url = models.URLField()
    source = models.CharField(max_length=100, blank=True, null=True, help_text="Optional: Source of this download")
    
    class Meta:
        unique_together = ('episode', 'quality')
        
    def __str__(self):
        return f"{self.episode} - {self.get_quality_display()}"

class BongoMovie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.PositiveIntegerField()
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        null=True,
        blank=True
    )
    poster_image = models.ImageField(upload_to='bongomovie_posters/', null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    backdrop_image = models.ImageField(upload_to='bongomovie_backdrops/', null=True, blank=True)
    backdrop_url = models.URLField(null=True, blank=True)
    trailer_url = models.CharField(max_length=100, help_text="YouTube video ID", null=True, blank=True)
    download_url = models.URLField(null=True, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)
    director = models.CharField(max_length=200, blank=True)
    cast = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre)
    is_4k = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    def get_poster(self):
        return self.poster_image.url if self.poster_image else self.poster_url

    def get_backdrop(self):
        return self.backdrop_image.url if self.backdrop_image else self.backdrop_url

class LiveStream(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='livestream_videos/', help_text="Upload video file for live streaming (e.g., MP4, WebM)" , default='')
    poster_image = models.ImageField(upload_to='livestream_posters/', null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    backdrop_image = models.ImageField(upload_to='livestream_backdrops/', null=True, blank=True)
    backdrop_url = models.URLField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    is_live = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_poster(self):
        return self.poster_image.url if self.poster_image else self.poster_url

    def get_backdrop(self):
        return self.backdrop_image.url if self.backdrop_image else self.backdrop_url

    def get_video(self):
        return self.video_file.url if self.video_file else None