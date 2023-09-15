from rest_framework import serializers
from users.models import Account
from . models import Comment, Post

class AccountSerializer(serializers.ModelSerializer):
    total_posts = serializers.SerializerMethodField()
    
    def get_total_posts(self, obj):
        return obj.posts.filter(is_deleted=False).count() 

    class Meta:
        model = Account
        fields = ['id','username','first_name','last_name','email','profile_pic',
                  'total_posts',
                  'last_login','is_admin','is_staff','is_active','is_superuser']



class CommentSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only = True) 
    created_time = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'body', 'created_at', 'created_time')
        
              


class  PostSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only = True)
    likes_count = serializers.SerializerMethodField()
    reports_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many = True,read_only = True)

    def get_likes_count(self, obj):
        return obj.total_likes()
    
    def get_reports_count(self, obj):
        return obj.total_reports()
    
    class Meta:
        model = Post
        fields = ('id', 'author','content', 'img', 'likes','created_time','reports_count','likes_count','comments','is_blocked')






        