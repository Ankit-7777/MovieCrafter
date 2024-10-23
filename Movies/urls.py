from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from rest_framework.routers import DefaultRouter
from Movies.views import (
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
    MovieViewSet,
    CommentViewSet,
    RatingViewSet,
)


router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'ratings', RatingViewSet)


urlpatterns = [
    
    # Template pages
    
    path('', include(router.urls)),

    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('auth/', UserAuthView.as_view(), name='user-auth'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('change-password/', UserChangePasswordView.as_view(), name='user-change-password'),
    path('send-password-reset-email/', SendPasswordResetEmailView.as_view(), name='send-password-reset-email'),
    path('password-reset/<uid>/<token>/', UserPasswordResetView.as_view(), name='password-reset'),
   

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




