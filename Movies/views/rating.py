from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from Movies.models import Rating
from Movies.serializers import RatingSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return ratings for the movies the user has rated."""
        return Rating.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new rating."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Set the user to the authenticated user
            return Response({
                "message": "Rating created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "error": "Unable to create rating. Please check the entered data.",
            "details": serializer.errors,
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def retrieve(self, request, pk=None):
        """Retrieve a specific rating."""
        try:
            rating = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(rating)
            return Response({
                "message": "Rating retrieved successfully.",
                "data": serializer.data
            })
        except Rating.DoesNotExist:
            return Response({"error": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Update an existing rating."""
        try:
            rating = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(rating, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Rating updated successfully.",
                    "data": serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Rating.DoesNotExist:
            return Response({"error": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        """Partially update an existing rating."""
        try:
            rating = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(rating, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Rating partially updated successfully.",
                    "data": serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Rating.DoesNotExist:
            return Response({"error": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk=None):
        """Delete a rating."""
        try:
            rating = self.get_queryset().get(pk=pk)
            rating.delete()
            return Response({"message": "Rating deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Rating.DoesNotExist:
            return Response({"error": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)
