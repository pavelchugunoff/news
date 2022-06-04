from django.urls import path

from posts.views import CreatePostView, EditPostView, FavoritePostAPIView, GetPostsAPIView, PostRetrieveUpdateAPIView, CreatePostAPIView, PostView, RatePostAPIView, RemovePostAPIView

urlpatterns = [
    path('api/create/', CreatePostAPIView.as_view()),
    path('api/update/', PostRetrieveUpdateAPIView.as_view()),
    path('api/getposts/', GetPostsAPIView.as_view()),
    path('api/<slug:title_url>/rate/', RatePostAPIView.as_view()),
    path('api/<slug:title_url>/favorite/', FavoritePostAPIView.as_view()),
    path('api/<slug:title_url>/delete/', RemovePostAPIView.as_view()),
    path('<slug:title_url>/edit/', EditPostView),
    path('<slug:title_url>', PostView),
    path('create/', CreatePostView),   
    
]