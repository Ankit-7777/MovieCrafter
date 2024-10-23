from .user_profile import (
    UserProfileView,
    UserAuthView,
    UserUpdateView,
    UserChangePasswordView,
    SendPasswordResetEmailView,
    UserPasswordResetView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .movie import MovieViewSet
from .comment import CommentViewSet
from .rating import RatingViewSet