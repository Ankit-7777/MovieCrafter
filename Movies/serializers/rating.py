from rest_framework import serializers
from Movies.models import Rating, Movie

class RatingSerializer(serializers.ModelSerializer):
    # Optional: Include the movie title in the serializer
    movie_title = serializers.CharField(source='movie.name', read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'movie', 'movie_title', 'user', 'rating', 'review', 'created_date']
        read_only_fields = ['user', 'created_date']  # User and created_date are read-only

    def validate_rating(self, value):
        """Ensure rating is between 1 and 7."""
        if value < 1 or value > 7:
            raise serializers.ValidationError("Rating must be between 1 and 7.")
        return value

    def create(self, validated_data):
        """Set the user on create."""
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Custom update method if needed."""
        instance.rating = validated_data.get('rating', instance.rating)
        instance.review = validated_data.get('review', instance.review)
        instance.save()
        return instance

