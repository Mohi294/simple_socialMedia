from django.contrib import admin
from django.urls import path
import user.views as user_views
import post_manager.views as post_views
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    # login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # user
    path('api/users/register/',
         user_views.CreateUserView.as_view(), name='user_register'),
    path('api/change_password/<int:pk>/', user_views.ChangePasswordView.as_view(),
         name='auth_change_password'),
    path('api/update_profile/<int:pk>/', user_views.UpdateProfileView.as_view(),
         name='auth_update_profile'),
    # post
    path('api/post/create/', post_views.CreatePost.as_view(), name='create_post'),
    path('api/post/Repost/<int:post_id>/',
         post_views.CreateRepost.as_view(), name='Repost'),
    path('api/post/delete_post/<int:post_id>/', post_views.DeletePost.as_view(), name='delete_post'),
    path('api/post/undo_repost/<int:post_id>/', post_views.UndoRepost.as_view(), name='undo_repost'),
    path('api/post/show_posts/', post_views.ShowAllPosts.as_view(), name='show_all_posts'),
    # comment
    path('api/post/comment/', post_views.AddComment.as_view(), name='comment'),
    path('api/post/delete_comment/<int:comment_id>/', post_views.DeleteComment.as_view(), name='delete_comment')


]
