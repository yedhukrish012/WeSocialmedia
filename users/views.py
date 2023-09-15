from rest_framework.response import Response
from rest_framework import permissions,status,generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import permissions,status
from posts.models import Post
from posts.serializer import PostSerializer
from users.models import Account

from users.serializer import AccountCreateSerializer, AccountSerializer
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['email'] = user.email
        # ...
        usr = AccountSerializer(user)
        if usr.data['is_active']:
            return token
        else:
            return Response('You are Blocked by Admin',status=status.HTTP_404_NOT_FOUND)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET','POST'])
def getRoutes(request):
    routes = [
        'api/token/',
        'api/token/refresh/',
        'api/token/verify/',
        'register/',
        'users/me/'
    ]
    
    return Response(routes)


class RegisterUser(APIView):
    def post(self,request):
        serializer = AccountCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        user = serializer.create(serializer.validated_data)
        user = AccountSerializer(user)
        return Response(user.data,status=status.HTTP_201_CREATED)
    
class RetrieveUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user = AccountSerializer(user)
        return Response(user.data, status=status.HTTP_200_OK)
    




class ListUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = Account.objects.all()
        serializer = AccountSerializer(users, many=True)
        return Response(serializer.data)
    

class BlockUnblockUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, user_id):
        try:
            user = Account.objects.get(id=user_id)
            if user.is_active:
                user.is_active = False
                action = 'blocked'
            else:
                user.is_active = True
                action = 'unblocked'
            user.save()
            return Response({'message': f'User {user.username} is {action}.'}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        


        
class PostsList(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self,request):
        try:
            posts = Post.objects.filter(is_deleted=False).order_by('-created_at')
            serializer = PostSerializer(posts, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class BlockPost(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def post(self,request,id):
        try:
            post=Post.objects.get(id=id)
            if post.is_blocked:
                post.is_blocked=False
            else:
                post.is_blocked=True
            post.save()
            return Response('Sucess',status=status.HTTP_200_OK)
                
        except Post.DoesNotExist:
            return Response('Post not Exist',status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response('somthing Went wrong',str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BlockedPostsList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.filter(is_blocked=True).order_by('-created_at')
    serializer_class = PostSerializer
    


class ReportedPostsList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset =Post.objects.filter(reports__isnull=False).exclude(is_deleted = True,is_blocked=True,).order_by('-created_at')
    serializer_class = PostSerializer
        