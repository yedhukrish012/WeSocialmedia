from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from users.views import (
    BlockPost,
    BlockUnblockUserView,
    BlockedPostsList,
    ListUsersView,
    MyPostListAPIView,
    ReportedPostsList,
    RetrieveUserView,
    RegisterUser,
    UpdateProfilePicView,
    getRoutes,
)


urlpatterns = [
    path("", getRoutes, name="getRoutes"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("users/me/", RetrieveUserView.as_view(), name="getRoutes"),
    path("update-profile-pic/", UpdateProfilePicView.as_view(), name="update-profile-pic"),

    path("listusers/", ListUsersView.as_view(), name="ListUsersView"),
    path("action/<int:user_id>/",BlockUnblockUserView.as_view(),name="block-unblock-user",),

    
    # path("listpost/", PostsList.as_view(), name="postslist"),
    path("blockpost/<str:id>/", BlockPost.as_view(), name="blockpost"),
    path("blockedposts/", BlockedPostsList.as_view(), name="blockedpostslist"),
    path("listreportedposts/", ReportedPostsList.as_view(), name="reportedpostslist"),
    path("posts/", MyPostListAPIView.as_view(), name="post-list"),
]
