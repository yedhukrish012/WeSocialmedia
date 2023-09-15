from rest_framework.response import Response
from rest_framework import permissions,status,generics
from posts.models import Post
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from posts.serializer import PostSerializer
from django.shortcuts import get_object_or_404 

# Create your views here.
class PostListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.filter(is_deleted=False, is_blocked=False).order_by('-created_at')
    serializer_class = PostSerializer


class CreatePostView(APIView):
    permission_classes  = [permissions.IsAuthenticated]
    serializer_class    = PostSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            post = serializer.save(author=request.user)
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class UpdatePostView(UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  

    def get_queryset(self):
        return Post.objects.all().exclude(is_deleted=True)

    def update(self, request, id):
        try:
            
            instance = self.get_object()
            if request.user == instance.author or request.user.is_superuser:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                return Response("you are not allowed edit it")
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        


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


class ReportPostView(APIView):
    def post(self,request,id):
        try:
            post = Post.objects.get(id=id)
            if request.user in post.reports.all():
                return Response("You have already reported this post.", status=status.HTTP_400_BAD_REQUEST)
            post.reports.add(request.user)                  
            return Response("Post Reported", status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response("Post not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    