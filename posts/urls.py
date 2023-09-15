from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostListView.as_view(), name='list_posts'),
    path('create-post/', views.CreatePostView.as_view(), name='create-posts'),
    path('update-post/<int:id>/', views.UpdatePostView.as_view(), name='update-post'),
    path('delete/<int:id>/', views.DeletePostView.as_view(), name='delete-post'),
    path('report/<int:id>/', views.ReportPostView.as_view(), name='report-post'),
]
