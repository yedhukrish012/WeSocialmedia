from . import views
from django.urls import path


urlpatterns = [
    path("", views.PostListView.as_view(), name="list_posts"),
    path("create-post/", views.CreatePostView.as_view(), name="create-posts"),
    path("update-post/<int:id>/", views.UpdatePostView.as_view(), name="update-post"),
    path('getpost/<int:id>/', views.PostDetailView.as_view(), name='post-detail'),
    path("delete/<int:id>/", views.DeletePostView.as_view(), name="delete-post"),
    path("report/<int:id>/", views.ReportPostView.as_view(), name="report-post"),
    path("like/<int:id>/", views.LikePostView.as_view(), name="like-post"),
  

    path('create-comment/<int:id>/', views.CreateComment.as_view(), name='add-comment'),
    path('delete-comment/<int:id>/', views.DeleteComment.as_view(), name='delete-comment'),
    path('comments/<int:id>/', views.CommentList.as_view(), name='comment-list-by-created-time'),
    
    path('follow/<int:user_id>/', views.FollowUnfollowUserView.as_view(), name='follow-user'),
    path('followings/<int:id>/', views.FollowingListView.as_view(), name='following-list'),
    path('followers/<int:id>/', views.FollowerListView.as_view(), name='follower-list'),
]
