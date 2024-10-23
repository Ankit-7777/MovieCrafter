from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from Movies.models import Movie
from Movies.serializers import MovieSerializer
from Movies.pagination import MyPageNumberPagination
from  Movies.permissions import IsOwnerOrReadOnly 

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [ IsOwnerOrReadOnly]
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Movie.objects.all().order_by('release_date')
        return Movie.objects.filter(director=self.request.user).order_by('release_date')

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id 

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({
                "message": "Comment created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "error": "Unable to create comment.",
            "details": serializer.errors,
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Movie records fetched successfully.",
            "data": serializer.data
        })

    def retrieve(self, request, pk=None):
        try:
            movie = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(movie)
            return Response({"message": "Movie retrieved successfully.", "data": serializer.data})
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found with the provided ID."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            movie = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()  # Save updated movie instance
                return Response({"message": "Movie updated successfully.", "data": serializer.data})
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found with the provided ID."}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            movie = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(movie, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # Save partial updates
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found with the provided ID."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            movie = self.get_queryset().get(pk=pk)
            movie.delete()
            return Response({"message": "Movie deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found with the provided ID."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({'error': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(name__icontains=query)  # Search by movie name
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response({"message": "Search completed successfully.", "data": serializer.data})
        
        return Response({"message": "No movies found matching the search criteria."})
