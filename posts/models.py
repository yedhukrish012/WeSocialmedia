from datetime import timezone
from django.db import models
from django.utils.timesince import timesince
from users.models import Account


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Account, related_name="posts", on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to="posts/")
    likes = models.ManyToManyField(Account, related_name="liked_posts", blank=True)
    reports = models.ManyToManyField(Account, related_name="reported_posts", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.author.username

    def total_likes(self):
        return self.likes.count()

    def created_time(self):
        return timesince(self.created_at)

    def total_reports(self):
        return self.reports.count()


class Comment(models.Model):
    user = models.ForeignKey(Account, related_name="author", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

    def created_time(self):
        return timesince(self.created_at)


class Follow(models.Model):
    follower = models.ForeignKey(
        Account, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        Account, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()




class Notification(models.Model):
   NOTIFICATION_TYPES = [
        ('like', 'New Like'),
        ('post', 'New Post'),
        ('follow', 'New Follow'),
        ('comment', 'New Comment'),
        ('blocked', 'Post Blocked'),
        ('unblocked', 'Post Unblocked'),
    ]
   
   from_user = models.ForeignKey(Account, related_name="notification_from", on_delete=models.CASCADE, null=True)
   to_user = models.ForeignKey(Account, related_name="notification_to", on_delete=models.CASCADE, null=True)
   notification_type = models.CharField(choices=NOTIFICATION_TYPES, max_length=20)
   post  = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
   comment  = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
   created = models.DateTimeField(auto_now_add=True)
   is_seen = models.BooleanField(default=False)
   
   def __str__(self):
        return f"{self.from_user} sent a {self.notification_type} notification to {self.to_user}"