from rest_framework import serializers
from users.models import Account
from .models import Comment, Follow, Post


#-------------------------------------------------------------------------------------Account Settings----------------------------------------------#

class AccountSerializer(serializers.ModelSerializer):
    total_posts = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()

    def get_total_posts(self, obj):
        return obj.posts.filter(is_deleted=False).count()
    
    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.following.count()  

    class Meta:
        model = Account
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_pic",
            "total_posts",
            "last_login",
            "is_admin",
            "is_staff",
            "is_active",
            "is_superuser",
            "followers_count",
            "followings_count",
        ]





#-------------------------------------------------------------------------Post and comment----------------------------------------------------------------#

class CommentSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id",  "user", "content", "created_time")



class PostSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    reports_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    is_following_author = serializers.SerializerMethodField()
    img = serializers.ImageField(required=False)  # New field

    def get_likes_count(self, obj):
        return obj.total_likes()

    def get_reports_count(self, obj):
        return obj.total_reports()

    def get_is_following_author(self, obj):
        user = self.context['request'].user
        author = obj.author
        if user.is_authenticated:
            try:
                follow_instance = Follow.objects.get(follower=user, following=author)
                return True
            except Follow.DoesNotExist:
                return False
        return False

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "content",
            "img",
            "likes",
            "created_time",
            "reports_count",
            "likes_count",
            "comments",
            "is_blocked",
            "is_following_author",  # Include the new field
        )



#---------------------------------------------------------------------------Follow Settings--------------------------------------------------------------------------------------#

class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field="email", queryset=Account.objects.all()
    )
    follower = serializers.SlugRelatedField(
        slug_field="email", queryset=Account.objects.all()
    )

    class Meta:
        model = Follow
        fields = ["follower", "following", "created_at"]


# serializers.py

class FollowerSerializer(serializers.ModelSerializer):
    follower = AccountSerializer(read_only=True)
    is_following_follower = serializers.SerializerMethodField()

    def get_is_following_follower(self, obj):
        user = self.context['request'].user
        follower = obj.follower
        if user.is_authenticated:
            try:
                follow_instance = Follow.objects.get(follower=user, following=follower)
                return True
            except Follow.DoesNotExist:
                return False
        return False

    class Meta:
        model = Follow
        fields = ["follower", "created_at", "is_following_follower"]


class FollowingSerializer(serializers.ModelSerializer):
    following = AccountSerializer( read_only=True)

    class Meta:
        model = Follow
        fields = ["following", "created_at"]










