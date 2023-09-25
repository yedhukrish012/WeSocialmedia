from django.contrib import admin

from posts.models import Comment, Follow, Post


# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
