from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['username', 'email']

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user_username', 'date_of_birth', 'bio', 'country', 'verified']

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['auth_username', 'title', 'description']

    def auth_username(self, obj):
        return obj.user.username
    auth_username.short_description = 'Username'


# class CommentAdmin(admin.ModelAdmin):
#     model = Comment
#     list_display = ['']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)