from django.contrib import admin
from .models import Profile, Video, Comment, Like, Subscription

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user__username']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'uploaded_at', 'views']
    search_fields = ['title', 'user__username']
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ['uploaded_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'timestamp']
    search_fields = ['user__username', 'video__title']
    list_filter = ['timestamp']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'created_at']
    search_fields = ['user__username', 'video__title']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'channel', 'subscribed_at']
    search_fields = ['subscriber__username', 'channel__username']
