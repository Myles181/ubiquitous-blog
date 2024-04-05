from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView
)



urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('test/', views.protected_routes, name='test'),
    path('profile/<int:user_id>/', views.getProfile, name='get_profile'),
    path('profile/update/<int:user_id>', views.updateProfile, name='update_profile'),
    path('posts/', views.getPost_all, name='get_all_post'),
    path('posts/<int:user_id>', views.getPost_by_id, name='get_id_post'),
    path('post/create/', views.createPost, name='create_post'),
    path('post/<int:post_id>/edit/', views.editPost, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delPost, name='delete_post'),
    path('post/<int:post_id>/comments/', views.getPostComments, name='get_post_comments'),
    path('comment/<int:post_id>/create/', views.createPostComment, name='create_comment'),
    path('comment/<int:comment_id>/edit/', views.editPostComment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.deletePostComment, name='delete_comment'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/dislike/', views.dislike_comment, name='dislike_comment'),
]

# path('', views.get_routes, name='get_routes'),
# path('search/', search_posts, name='search_posts'),
# path('notifications/', notifications, name='notifications'),
# path('send_verification_code/', send_verification_code, name='send_verification_code'),
# path('verify_email/', verifyEmail, name='verify_email'),