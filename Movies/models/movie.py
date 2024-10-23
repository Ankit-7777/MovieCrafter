from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
from moviepy.editor import VideoFileClip
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.conf import settings

def validate_trailer_video_duration(video):
    if isinstance(video, InMemoryUploadedFile):
        try:
            clip = VideoFileClip(video.temporary_file_path())
            if clip.duration < 10 or clip.duration > 30:
                raise ValidationError("Trailer video duration must be between 10 and 30 seconds.")
        except Exception as e:
            raise ValidationError(f"Error processing trailer video file: {e}")


def validate_full_movie_video_duration(video):
    if isinstance(video, InMemoryUploadedFile):
        try:
            clip = VideoFileClip(video.temporary_file_path())
            if clip.duration < 1800:  # 30 minutes in seconds
                raise ValidationError("Full movie video duration must be at least 30 minutes.")
        except Exception as e:
            raise ValidationError(f"Error processing full movie video file: {e}")


class Movie(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    director = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poster = models.ImageField(upload_to='post_images/', blank=True, null=True)
    trailer_video = models.FileField(upload_to='trailer_videos/', blank=True, null=True,
                                      validators=[validate_trailer_video_duration])
    full_movie_video = models.FileField(upload_to='full_movies/', blank=True, null=True,
                                         validators=[validate_full_movie_video_duration])
    release_date = models.DateField()
    language = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=7, decimal_places=1, default=0.0)
    tags = TaggableManager()
    views_count = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.pk})