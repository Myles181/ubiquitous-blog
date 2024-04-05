from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['id', 'username', 'email']

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user_username', 'date_of_birth', 'bio', 'country', 'verified']

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['id', 'auth_username', 'title']

    def auth_username(self, obj):
        return obj.author.username
    auth_username.short_description = 'Username'


class CommentAdmin(admin.ModelAdmin):
    model = PostComment
    list_display = ['id', 'body', 'auth_username', 'post']

    def auth_username(self, obj):
        return obj.author.username
    auth_username.short_description = 'Username'

    def post(self, obj):
        return obj.post.title
    post.short_description = 'Post'



admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, CommentAdmin)

