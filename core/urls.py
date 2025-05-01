from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<slug:slug>/', views.video_detail, name='video_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.search_videos, name='search_videos'),
    path('video/<slug:slug>/like/', views.toggle_like, name='toggle_like'),
    path('search/', views.search_videos, name='search_videos'),
]
