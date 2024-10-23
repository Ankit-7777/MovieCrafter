from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from Movies.models import Comment
from Movies.serializers import CommentSerializer
from django.shortcuts import get_object_or_404

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """ Return comments related to a specific movie if provided. """
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id:
            return self.queryset.filter(movie_id=movie_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        """ Create a new comment. """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # Automatically set the author to the logged-in user
            return Response({"message": "Comment created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": "Unable to create comment.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ Retrieve a specific comment by ID. """
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.get_serializer(comment)
        return Response({"message": "Comment retrieved successfully.", "data": serializer.data})

    def update(self, request, pk=None):
        """ Update an existing comment (full update). """
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.get_serializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment updated successfully.", "data": serializer.data})
        return Response({"error": "Unable to update comment.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """ Partially update an existing comment. """
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.get_serializer(comment, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment partially updated successfully.", "data": serializer.data})
        return Response({"error": "Unable to partially update comment.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ Delete a comment. """
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
