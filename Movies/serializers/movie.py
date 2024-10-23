from rest_framework import serializers
from Movies.models import Movie
from django.utils import timezone

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_trailer_video(self, value):
        """
        Validate the trailer video duration.
        """
        if value:
            validate_trailer_video_duration(value)
        return value

    def validate_full_movie_video(self, value):
        """
        Validate the full movie video duration.
        """
        if value:
            validate_full_movie_video_duration(value)
        return value

    def validate(self, attrs):
        """
        Additional validations can be performed here.
        """
        if 'release_date' in attrs and attrs['release_date'] < timezone.now().date():
            raise serializers.ValidationError("The release date cannot be in the past.")
        return attrs

