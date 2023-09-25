from rest_framework.response import Response
from rest_framework import permissions, status, generics
from posts.models import Comment, Follow, Post
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from posts.serializer import (
    CommentSerializer,
    FollowerSerializer,
    FollowingSerializer,
    PostSerializer,
)
from django.shortcuts import get_object_or_404

from users.models import Account


# Create your views here.
class PostListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.filter(is_deleted=False, is_blocked=False).order_by(
        "-created_at"
    )
    serializer_class = PostSerializer


class CreatePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            post = serializer.save(author=request.user)
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePostView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_deleted=False, is_blocked=False)
    lookup_field = "id"

    def perform_update(self, serializer):
        instance = self.get_object()
        if "img" in self.request.data and self.request.data["img"] != "":
            img = self.request.data["img"]
        else:
            img = instance.img
        serializer.save(img=img)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.author:
            return self.update(request, *args, **kwargs)
        else:
            return Response(
                "You are not allowed to update this post.",
                status=status.HTTP_403_FORBIDDEN,
            )


class DeletePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().exclude(is_deleted=True)

    def get_object(self, id):
        return get_object_or_404(self.get_queryset(), id=id)

    def delete(self, request, id):
        try:
            instance = self.get_object(id)
            if request.user == instance.author or request.user.is_superuser:
                post = Post.objects.get(id=id)
                post.is_deleted = True
                post.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response("you are not allowed delete it")
        except Post.DoesNotExist:
            return Response("No such post found.", status=status.HTTP_404_NOT_FOUND)


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        try:
            post = self.get_object()
            serializer = self.get_serializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ReportPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        try:
            post = Post.objects.get(id=id)
            if request.user in post.reports.all():
                return Response(
                    "You have already reported this post.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            post.reports.add(request.user)
            return Response("Post Reported", status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response("Post not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        try:
            post = Post.objects.get(id=id)

            if request.user in post.likes.all():
                post.likes.remove(request.user)
                return Response("unliked post", status=status.HTTP_200_OK)
            else:
                post.likes.add(request.user)
                return Response("Liked Post", status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response("Post not found", status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class FollowUnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        logged_in_user = request.user
        try:
            user_to_follow = Account.objects.get(id=user_id)
        except Account.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if logged_in_user == user_to_follow:
            return Response(
                {"detail": "You cannot follow/unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            follow_instance = Follow.objects.get(
                follower=logged_in_user, following=user_to_follow
            )
            follow_instance.delete()
            return Response(
                {"detail": "You have unfollowed this user."}, status=status.HTTP_200_OK
            )
        except Follow.DoesNotExist:
            follow_instance = Follow(follower=logged_in_user, following=user_to_follow)
            follow_instance.save()
            return Response(
                {"detail": "You are now following this user."},
                status=status.HTTP_201_CREATED,
            )


class CreateComment(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request, id, *args, **kwargs):
        try:
            user = request.user
            content = request.data["content"]
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user, post_id=id, content=content)
                return Response({"comment Done"}, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE
                )
        except Exception as e:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


class DeleteComment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        try:
            comment = Comment.objects.get(id=id, user=request.user)
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response("No such comment found.!", status=status.HTTP_404_NOT_FOUND)


class CommentList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request, id):
        try:
            post = get_object_or_404(Post, id=id)
            queryset = Comment.objects.filter(post=post).order_by("created_at")
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FollowerListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user_id = self.kwargs["id"]
        user = Account.objects.get(id=user_id)
        return Follow.objects.filter(following=user)


class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowingSerializer

    def get_queryset(self):
        user_id = self.kwargs["id"]
        user = Account.objects.get(id=user_id)
        return Follow.objects.filter(follower=user)
